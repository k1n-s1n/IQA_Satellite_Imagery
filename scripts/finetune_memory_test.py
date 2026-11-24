"""Fine-tuning memory test for DiffusionSat.

Runs a few real training steps (forward, loss, backward, optimizer step) on random
tensors with the same shapes as real data, and records peak GPU memory and time per
step for each setting in the config. It mirrors the training step in DiffusionSat's
train_text_to_image.py (noise-prediction MSE loss; SNR weighting left out because it
does not change memory). No useful learning happens; weights are discarded.

Usage (from the repo root, in the diffusionsat conda env):
    python scripts/finetune_memory_test.py --config configs/finetune_memory_test.yaml
"""
import argparse
import csv
import gc
import json
import os
import time
from copy import deepcopy

import yaml


def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def make_optimizer(name, params, lr):
    if name == "adamw":
        return torch.optim.AdamW(params, lr=lr)
    if name == "adamw8bit":
        import bitsandbytes as bnb  # may not install on Windows
        return bnb.optim.AdamW8bit(params, lr=lr)
    raise ValueError(f"Unknown optimizer: {name}")


def free_memory():
    gc.collect()
    torch.cuda.empty_cache()


def run_one(cfg, run, shared):
    """One setting: load a fresh UNet, train on random batches, return measurements."""
    device = shared["device"]
    bs = run["batch_size"]
    gen = torch.Generator(device=device).manual_seed(cfg["seed"])

    unet = optimizer = ema_unet = None
    try:
        # Trainable UNet in fp32 (master weights); fp16 only inside autocast, as accelerate does
        unet = SatUNet.from_pretrained(
            cfg["unet_path"], subfolder="unet",
            num_metadata=cfg["num_metadata"], use_metadata=cfg["num_metadata"] > 0,
            low_cpu_mem_usage=False,
        ).to(device)
        unet.train()
        if run["grad_checkpointing"]:
            unet.enable_gradient_checkpointing()
        if run["ema"]:
            ema_unet = EMAModel(deepcopy(unet).parameters())
            ema_unet.to(device)
        optimizer = make_optimizer(run["optimizer"], unet.parameters(), cfg["learning_rate"])
        scaler = torch.cuda.amp.GradScaler()

        # Random inputs with the real shapes
        pixel_values = torch.rand(bs, 3, cfg["resolution"], cfg["resolution"],
                                  generator=gen, device=device) * 2 - 1      # images in [-1, 1]
        input_ids = shared["input_ids"].repeat(bs, 1)                       # (bs, 77) tokens
        metadata = torch.randn(bs, cfg["num_metadata"], generator=gen, device=device)

        free_memory()
        torch.cuda.reset_peak_memory_stats()
        step_times = []
        total_steps = cfg["warmup_steps"] + cfg["timed_steps"]

        for step in range(total_steps):
            torch.cuda.synchronize()
            t0 = time.perf_counter()

            with torch.no_grad():  # frozen VAE and text encoder
                latents = shared["vae"].encode(pixel_values.half()).latent_dist.sample()
                latents = latents * shared["vae"].config.scaling_factor
                encoder_hidden_states = shared["text_encoder"](input_ids)[0]

            noise = torch.randn_like(latents)
            timesteps = torch.randint(0, shared["scheduler"].config.num_train_timesteps,
                                      (bs,), device=device).long()
            noisy_latents = shared["scheduler"].add_noise(latents, noise, timesteps)
            if shared["scheduler"].config.prediction_type == "v_prediction":
                target = shared["scheduler"].get_velocity(latents, noise, timesteps)
            else:
                target = noise

            with torch.autocast("cuda", dtype=torch.float16):
                model_pred = unet(noisy_latents, timesteps, encoder_hidden_states,
                                  metadata=metadata).sample
            loss = F.mse_loss(model_pred.float(), target.float())

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(unet.parameters(), cfg["max_grad_norm"])
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad(set_to_none=True)
            if ema_unet is not None:
                ema_unet.step(unet.parameters())

            torch.cuda.synchronize()
            if step >= cfg["warmup_steps"]:
                step_times.append(time.perf_counter() - t0)

        return {
            "status": "ok",
            "peak_allocated_gb": round(torch.cuda.max_memory_allocated() / 1024**3, 2),
            "peak_reserved_gb": round(torch.cuda.max_memory_reserved() / 1024**3, 2),
            "sec_per_step": round(sum(step_times) / len(step_times), 3),
            "final_loss": round(loss.item(), 4),
            "error": "",
        }
    except torch.cuda.OutOfMemoryError:
        return {"status": "oom", "error": "CUDA out of memory"}
    except ImportError as e:
        return {"status": "skipped", "error": f"ImportError: {e}"}
    finally:
        del unet, optimizer, ema_unet
        free_memory()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_config(args.config)
    os.environ.setdefault("HF_HOME", cfg["hf_home"])

    # Heavy imports after HF_HOME is set
    global torch, F, SatUNet, EMAModel
    import torch
    import torch.nn.functional as F
    from transformers import CLIPTextModel, CLIPTokenizer
    from diffusers import AutoencoderKL, DDPMScheduler
    from diffusers.training_utils import EMAModel
    from diffusionsat.sat_unet import SatUNet

    torch.manual_seed(cfg["seed"])
    device = "cuda"

    # Frozen parts, loaded once and shared by every run (fp16, like weight_dtype in training)
    tokenizer = CLIPTokenizer.from_pretrained(cfg["pipeline_path"], subfolder="tokenizer")
    shared = {
        "device": device,
        "scheduler": DDPMScheduler.from_pretrained(cfg["pipeline_path"], subfolder="scheduler"),
        "vae": AutoencoderKL.from_pretrained(cfg["pipeline_path"], subfolder="vae",
                                             torch_dtype=torch.float16).to(device).requires_grad_(False),
        "text_encoder": CLIPTextModel.from_pretrained(cfg["pipeline_path"], subfolder="text_encoder",
                                                      torch_dtype=torch.float16).to(device).requires_grad_(False),
        "input_ids": tokenizer("a satellite image", padding="max_length",
                               max_length=tokenizer.model_max_length, truncation=True,
                               return_tensors="pt").input_ids.to(device),
    }

    os.makedirs(cfg["output_dir"], exist_ok=True)
    fields = ["group", "batch_size", "grad_checkpointing", "ema", "optimizer", "status",
              "peak_allocated_gb", "peak_reserved_gb", "sec_per_step", "final_loss", "error"]
    results, failed_groups = [], set()

    for run in cfg["runs"]:
        if run["group"] in failed_groups:
            row = {**run, "status": "not_run", "error": "earlier run in group ran out of memory"}
        else:
            print(f"Running {run} ...", flush=True)
            row = {**run, **run_one(cfg, run, shared)}
            if row["status"] == "oom":
                failed_groups.add(run["group"])
        print(row, flush=True)
        results.append(row)

    with open(os.path.join(cfg["output_dir"], "results.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    env = {
        "gpu": torch.cuda.get_device_name(0),
        "gpu_total_gb": round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 2),
        "torch": torch.__version__,
        "cuda": torch.version.cuda,
        "config": cfg,
    }
    with open(os.path.join(cfg["output_dir"], "env_info.json"), "w") as f:
        json.dump(env, f, indent=2)
    print(f"Saved results to {cfg['output_dir']}")


if __name__ == "__main__":
    main()
