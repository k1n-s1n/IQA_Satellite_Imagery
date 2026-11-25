# Sargassum baseline (pretrained DiffusionSat, no fine-tuning)

**Date:** Wed 25 Nov 2026
**Purpose:** See whether the pretrained DiffusionSat 256 model can generate ocean or sargassum-like images before any fine-tuning. Gives a baseline to compare fine-tuned models against.

## Setup
- Script: `scripts/sargassum_baseline.py`, config: `configs/sargassum_baseline.yaml` (full config also in `env_info.json`)
- Same model and settings as `results/diffusionsat_first_run/`: `checkpoint-150000/unet`, fp16, 256x256, 20 steps, guidance scale 7.5
- Grid: 2 prompts × 2 metadata conditions × 4 seeds (0–3) = 16 images
  - p0: "a satellite image of the ocean"
  - p1: "a satellite image of seaweed floating on the ocean"
  - `caribbean`: lon -64, lat 15, GSD 10 m, cloud cover 0, 15 June 2020 (raw values, normalised with `metadata_normalize`); an example open-water point, not a MARIDA tile
  - `dropped`: all-zero normalised metadata, passed without `metadata_normalize`

## Run 1 (`results/sargassum_baseline_run1/`)
- The second condition was `metadata=None`. All 8 of those runs failed with `AssertionError`: the pipeline requires metadata.
- In the training script, metadata is zeroed after normalisation for ~10% of samples (`keep_mask = torch.rand_like(metadata) > 0.1`), so all-zero normalised metadata is the model's learned "metadata dropped" input. I used that for run 2.

## Run 2 (this folder)
- All 16 images generated; ~0.7 s per image after the first (first includes CUDA warm-up), peak 2.61 GiB.
- The 8 Caribbean images are byte-identical to run 1: same seeds and settings give the same output.

## Observations (visual inspection only, no metrics yet)

| | Caribbean metadata | Dropped metadata |
| --- | --- | --- |
| p0 (ocean) | 3/4 harbours or coastlines with towns; 1/4 grey striped noise | 3/4 open water (waves, a boat wake, a small island); 1/4 grey texture with a dark blob |
| p1 (seaweed) | grey textures and blobs; 1/4 a grey coastal scene with roads | grey/dark textures and blobs; nothing sargassum-like |

- The Caribbean images look like sub-metre imagery (individual buildings and boats), not 10 m, so the model seems to ignore or not understand GSD = 10 m.
- No image looks like sargassum. The pretrained model cannot produce it from text and metadata alone, which supports fine-tuning on sargassum data.

## Open questions
- The Caribbean condition changed location and GSD together, so I can't tell which pushed the model towards harbours. Next: change one at a time (e.g. Caribbean location with ~1 m GSD vs 10 m).
- Did DiffusionSat's Satlas training data include Sentinel-2 (10 m)? Check Khanna et al. (2024).
- The seaweed prompt is not in the fMoW caption style ("a fmow satellite image of a ... in ..."); an fMoW-style prompt might behave differently.
