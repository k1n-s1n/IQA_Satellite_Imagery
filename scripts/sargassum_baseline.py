"""Pretrained DiffusionSat baseline for sargassum-like generation.

Runs every (prompt, metadata condition, seed) combination from the config with the
pretrained 256 checkpoint (no fine-tuning). Saves each image, a results.csv
(settings, time, peak VRAM, status) and env_info.json.

Usage (from repo root, lab PC):
    python scripts/sargassum_baseline.py --config configs/sargassum_baseline.yaml
"""
import argparse
import csv
import json
import os
import time

import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    os.environ["HF_HOME"] = cfg["hf_home"]  # must be set before HF imports
    import torch
    # VERIFY: these imports match the ones in single-image.ipynb
    from diffusionsat import SatUNet, DiffusionSatPipeline, metadata_normalize

    out_dir = cfg["output_dir"]
    os.makedirs(out_dir, exist_ok=True)

    # Load the model as in the first run: unet (not unet_ema), fp16
    unet = SatUNet.from_pretrained(cfg["unet_path"], subfolder="unet", torch_dtype=torch.float16)
    pipe = DiffusionSatPipeline.from_pretrained(
        cfg["pipeline_path"], unet=unet, torch_dtype=torch.float16
    ).to("cuda")

    rows = []
    for p_idx, prompt in enumerate(cfg["prompts"]):
        for md_name, md in cfg["metadata_conditions"].items():
            # Dict order in the YAML = order passed to the model
            metadata = None if md is None else metadata_normalize(list(md.values())).tolist()
            for seed in cfg["seeds"]:
                name = f"p{p_idx}_{md_name}_seed{seed}.png"
                generator = torch.Generator("cuda").manual_seed(seed)
                torch.cuda.reset_peak_memory_stats()
                torch.cuda.synchronize()
                start = time.perf_counter()
                status = "ok"
                try:
                    image = pipe(
                        prompt,
                        metadata=metadata,
                        height=cfg["resolution"],
                        width=cfg["resolution"],
                        num_inference_steps=cfg["num_inference_steps"],
                        guidance_scale=cfg["guidance_scale"],
                        generator=generator,
                    ).images[0]
                    image.save(os.path.join(out_dir, name))
                except Exception as e:  # e.g. pipeline may not accept metadata=None
                    status = f"error: {type(e).__name__}: {e}"
                    name = ""
                torch.cuda.synchronize()
                rows.append({
                    "prompt_id": p_idx, "prompt": prompt, "metadata": md_name,
                    "seed": seed, "file": name, "status": status,
                    "time_s": round(time.perf_counter() - start, 2),
                    "peak_vram_gb": round(torch.cuda.max_memory_allocated() / 1024**3, 2),
                })
                print(rows[-1])

    with open(os.path.join(out_dir, "results.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    env = {
        "gpu": torch.cuda.get_device_name(0),
        "torch": torch.__version__,
        "cuda": torch.version.cuda,
        "config": cfg,
    }
    with open(os.path.join(out_dir, "env_info.json"), "w") as f:
        json.dump(env, f, indent=2)


if __name__ == "__main__":
    main()
