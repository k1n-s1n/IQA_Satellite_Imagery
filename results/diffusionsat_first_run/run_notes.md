# DiffusionSat — first generation run

**Date:** Thu 19 Nov 2026
**Purpose:** Confirm DiffusionSat inference works on a high-GPU university desktop before any fine-tuning.

## Hardware
- NVIDIA RTX A4000 (16 GB), Windows 11, driver CUDA 13.2

## Software
- Python 3.10 (conda env), PyTorch 2.2.2+cu121
- Pins: `numpy<2` (1.26.4), `huggingface_hub<0.26` (0.25.2)
- DiffusionSat installed editable from the GitHub ZIP (bundled diffusers 0.17)
- Full environment: `env_freeze.txt` (pip freeze)

## Model
- DiffusionSat 256x256 checkpoint, Zenodo record 13756199 (CC BY 4.0); code Apache-2.0
- `checkpoint-150000`, `unet` subfolder (not `unet_ema`, following the authors' notebook), fp16

## Generation settings
- Notebook: `notebooks/single-image.ipynb` (edited; SD 2.1 baseline cell skipped)
- Prompt: "a fmow satellite image of a electric substation in India" (authors' example)
- Metadata (raw, normalised with `metadata_normalize`): [76.5712666476, 28.6965307997, 0.929417550564, 0.0765712666476, 2015, 2, 27] (lon, lat, GSD, cloud cover, year, month, day)
- Guidance scale: 7.5
- Resolution: 256x256
- Inference steps: 20
- Seed: 42 (torch generator)

## Results
- Output: `first_image_seed42.png`
- Time: 1.6 s per image
- Peak VRAM: 2.81 GB (1e9 bytes) = 2.62 GiB; later scripts report GiB

## Notes
- Inference uses well under the 16 GB available; fine-tuning (gradients + optimizer states) not yet tested.
- Edited notebook not yet copied off the lab PC (C:\Temp is not safe storage).
