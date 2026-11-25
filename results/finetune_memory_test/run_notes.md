# Fine-tuning memory test

**Date:** Wed 25 Nov 2026
**Purpose:** Check whether the DiffusionSat 256 model can be fine-tuned on a high-GPU university desktop (16 GB) before preparing any training data. This is a memory and speed rehearsal, not real fine-tuning.

## Setup
- Script: `scripts/finetune_memory_test.py`, config: `configs/finetune_memory_test.yaml` (full config also in `env_info.json`)
- NVIDIA RTX A4000, 15.99 GiB total; PyTorch 2.2.2+cu121; same conda env as `results/diffusionsat_first_run/`
- Random tensors of the real shapes stand in for data (memory depends on tensor shapes, not pixel content)
- One training step mirrors the authors' `train_text_to_image.py`: fp32 UNet with fp16 autocast and GradScaler; VAE and text encoder fp16 and frozen; MSE noise-prediction loss
- 2 warm-up steps (not timed), then 5 timed steps; seed 42
- `diffusionsat` was not importable from the repo folder (`ModuleNotFoundError`), so I set `PYTHONPATH=C:\Temp\muhsin_fyp\DiffusionSat` in the prompt

## Results (`results.csv`)

| Group | Batch | EMA | Optimizer | Peak allocated (GiB) | Peak reserved (GiB) | s/step |
| --- | --- | --- | --- | --- | --- | --- |
| A | 1 | no | AdamW | 17.31 | 17.52 | 2.01 |
| A | 2 | no | AdamW | 17.31 | 17.54 | 2.53 |
| A | 4 | no | AdamW | 17.32 | 17.54 | 3.23 |
| A | 8 | no | AdamW | 17.34 | 17.57 | 5.86 |
| A | 16 | no | AdamW | 17.33 | 18.80 | 12.32 |
| B | 16 | yes | AdamW | 20.64 | 22.14 | 22.08 |
| C | 16 | no | 8-bit AdamW | skipped: bitsandbytes not installed | | |

All runs used gradient checkpointing. `results.csv` is from my second run of the test (re-run to watch Task Manager); the first run's printed values had the same memory figures and slightly different timings.

## Findings
- No run raised an out-of-memory error, but every run's peak exceeded the card's 15.99 GiB, even batch size 1.
- Task Manager showed dedicated GPU memory full (15.8/16.0 GB) and the overflow in shared GPU memory (system RAM), peaking at 7.1 GB during group B (`taskmanager_spillover_groupB.png`).
- So the timings include traffic to system RAM and are not true GPU speeds.
- Peak memory barely changes with batch size, so most of it is a fixed cost. My estimate (to verify): fp32 weights + gradients + two AdamW states ≈ 16 bytes × ~865M UNet parameters ≈ 13 GiB.

## Interpretation (to confirm)
- The spillover is most likely NVIDIA's "CUDA System Memory Fallback" driver setting on Windows (added in driver 536.40), which uses system RAM instead of raising out-of-memory. Not yet checked in the NVIDIA Control Panel on the lab PC.
- The authors' setup (batch 16 + EMA) does not fit on 16 GB. Options: memory savings (8-bit Adam, which needs bitsandbytes on Windows), turning the fallback off to find the true limit, or a larger GPU.
