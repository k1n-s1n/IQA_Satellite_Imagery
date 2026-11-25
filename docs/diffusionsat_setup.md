# DiffusionSat setup (Windows, high-GPU university desktop)

Set up on Thu 19 Nov 2026. This records how I built the environment so it can be rebuilt from scratch. The first generation run is recorded separately in `results/diffusionsat_first_run/run_notes.md`.

## 1. Hardware and constraints

- NVIDIA RTX A4000 (16 GB), Intel i7-13700, 32 GB RAM, Windows 11, driver CUDA 13.2
- Anaconda via AppsAnywhere (no admin rights)
- D: drive had only ~510 MB free, so everything went in `C:\Temp\muhsin_fyp\`. **This is not safe storage** (see section 7).

## 2. Environment

Redirect conda and pip caches away from the user profile (Anaconda Prompt):

```bat
set CONDA_PKGS_DIRS=C:\Temp\muhsin_fyp\conda_pkgs
set PIP_CACHE_DIR=C:\Temp\muhsin_fyp\pip_cache
conda create -p C:\Temp\muhsin_fyp\envs\diffusionsat python=3.10
conda activate C:\Temp\muhsin_fyp\envs\diffusionsat
```

Install PyTorch with CUDA 12.1 wheels (the driver supports newer CUDA, which is backward compatible):

```bat
pip install torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cu121
```

GPU check output: `2.2.2+cu121 True NVIDIA RTX A4000`.

## 3. DiffusionSat install

No git on the lab PC, so I downloaded the repository as a ZIP from GitHub and extracted it to `C:\Temp\muhsin_fyp\DiffusionSat\`. From that folder:

```bat
pip install -e ".[torch]"
pip install -r requirements_remaining.txt
```

## 4. Version conflicts

The DiffusionSat code dates from 2023, so two libraries had to be pinned to the older versions it was written against.

### `numpy<2` (installed 1.26.4)

- **Error:** on importing PyTorch, NumPy warned that a module compiled using NumPy 1.x cannot be run in NumPy 2.2.6 as it may crash, followed by `UserWarning: Failed to initialize NumPy: _ARRAY_API not found`.
- **Cause:** PyTorch 2.2.2 was built against NumPy 1.x, but pip installed the latest NumPy (2.2.6). NumPy 2 changed its internal interface, so PyTorch's links into NumPy break. The import still finished and the GPU check passed, but anything passing data between PyTorch and NumPy (such as loading or saving images) could fail.
- **Fix:** `pip install "numpy<2"`

### `huggingface_hub<0.26` (installed 0.25.2)

- **Error:** import failure on `cached_download` from `huggingface_hub` (exact message not recorded).
- **Cause:** the diffusers 0.17 bundled with DiffusionSat imports `cached_download`, which was removed in huggingface_hub v0.26.0 in favour of `hf_hub_download()` (huggingface_hub v0.26.0 release notes).
- **Fix:** `pip install "huggingface_hub<0.26"`

Full resulting environment: `results/diffusionsat_first_run/env_freeze.txt`.

## 5. Checkpoint

- DiffusionSat 256x256 checkpoint from Zenodo record 13756199: a single ~30 GB zip
- Contents: `checkpoint-100000` and `checkpoint-150000`, each with `unet`, `unet_ema` and optimizer states, plus a top-level diffusers pipeline
- Licences: weights CC BY 4.0, code Apache-2.0. Both are open; cite Khanna et al. (2024).

## 6. Notebook edits (`notebooks/single-image.ipynb`)

- Set `HF_HOME` to `C:/Temp/muhsin_fyp/hf_cache/` so Hugging Face downloads stay off the user profile
- Skipped the Stable Diffusion 2.1 baseline cell (not needed)
- Pointed the path at the nested checkpoint folder
- Loaded `SatUNet.from_pretrained(path + 'checkpoint-150000', subfolder="unet")` in fp16. I used `unet` rather than `unet_ema`, following the authors' notebook.
- Height/width 256, seeded generator (42), added timing

## 7. Known issues and next steps

- `C:\Temp` can be cleared: data, checkpoints and results to move to the X drive once DTS enlarges it; the conda env can stay local and be rebuilt from this doc
- Edited notebook copied to the repo on 25 Nov: `notebooks/single-image.ipynb`
- `diffusionsat` is not importable from outside the DiffusionSat folder (`ModuleNotFoundError` when running repo scripts), even though it was installed with `pip install -e`. The notebook only works because of its `sys.path.append('..')`. Workaround: `set PYTHONPATH=C:\Temp\muhsin_fyp\DiffusionSat` in the prompt before running repo scripts. Cause not yet checked (`pip show diffusionsat`).
- Inference uses 2.81 GB peak VRAM; fine-tuning memory (gradients + optimizer states) not yet tested on the A4000
