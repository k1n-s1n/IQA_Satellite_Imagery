# Data

Raw datasets are **not** committed. They are stored in OneDrive and gitignored.
Only small sample images go in `data/samples/`.

## Datasets

| Dataset | Status | Version | Link / DOI | Local path (OneDrive) | Notes |
| --- | --- | --- | --- | --- | --- |
| MARIDA (Marine Debris Archive) | Downloaded 13 Nov 2026 | 1.0.0 | [Zenodo](https://zenodo.org/records/5151941) · DOI: 10.5281/zenodo.5151941 | `Projects/Satellite_Imagery_FYP/MARIDA` (outside the repo) | Sentinel-2 patches with sargassum classes. Paper: Kikaki et al., 2022, PLOS ONE. 1,381 patches, 63 scenes; 114 patches contain sargassum; 5,154 sargassum pixels (`scripts/count_sargassum.py --pixels`, needs rasterio) |

## How to reproduce the data setup

*To be written once preprocessing scripts exist.*
