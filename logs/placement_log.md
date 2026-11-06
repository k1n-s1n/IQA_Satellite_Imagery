# Placement Log — Crocus / AI-INTERVENE

Research tasks, supervisor meetings and outputs. Total: 225 documented hours from 26 Oct 2026 to 26 Feb 2027, split into weeks, maximum 20 hours per week (Dr Wei, email 29 Oct 2026).

<!-- Entry template (newest at the bottom)
## Week N — w/c DD Mon YYYY — Hours: X / 20
| Date | Task | Hours |
| --- | --- | --- |
| | | |

**Reflection:** (what went well, issues/challenges)
-

**Way forward:**
-
**Next steps:**
-
-->

## Pre-placement work (before official start, 26 Oct 2026)

Work done while vetting/authorisation was pending, recorded under the real dates.
**Hours:** not claimed, pending confirmation with Dr Wei / HR. Estimates are for the record only.

### Week 1 — 6–11 Oct 2026 — Hours (estimate): 3

**Activities:**
- General background research in the field of satellite imagery, getting familiar with the topic.

**Reflection:**
- Getting oriented in a field that is new to me.

**Way forward:**
- Narrow the reading towards the applied case.

**Next steps:**
- Read further into sargassum and how it is monitored.

### Week 2 — 12–18 Oct 2026 — Hours (estimate): 2

**Activities:**
- Further reading on sargassum in the open sea and how it is monitored with satellite imagery.

**Reflection:**
- I don't fully understand all of it yet and need a simpler breakdown of the remote-sensing side.

**Way forward:**
- Revisit the sargassum material once I'm more comfortable with spectral bands.

**Next steps:**
- Look at accessible datasets and the standard image quality metrics.

### Week 3 — 19–25 Oct 2026 — Hours (estimate): 5

**Activities:**
- **Datasets researched:** Copernicus Data Space Ecosystem / Sentinel-2 (primary source of real multispectral imagery) and MARIDA (Sentinel-2 benchmark with a Sargassum class; most directly relevant to my applied case).
- **Metrics researched:** intro to PSNR and SSIM, and their limits for multispectral satellite data.
- **Thu 22 Oct, supervisor meeting with Dr Wei:** focus on Sentinel-2 and the sargassum class; generate my own synthetic dataset down the line and compare it with real data using insight-giving metrics; use a diffusion model rather than a GAN. Notes in `docs/supervisor_direction.md`.
- **Outputs:** project repo mirrored on GitLab and GitHub with skeleton (`.gitignore`, READMEs, logs, `docs/`); Research Notebook started.

**Reflection:**
- Standard metrics judge visual similarity and ignore spectral consistency and geospatial integrity, which is the gap this research targets.
- I now have a clearer picture of what the role wants from me and which direction to head.

**Way forward:**
- Investigate two open questions: paired vs unpaired metrics, and RGB vs multispectral generation.

**Next steps:**
- Read and break down DiffusionSat.
- Confirm with Dr Wei whether pre-start hours count, and the logbook format.

## Week 1 — w/c 26 Oct 2026 — Hours: 13 ( Total so far: 13/225)

| Date | Task | Hours |
| --- | --- | --- |
| Mon 26 Oct | Read Wang et al. (2019), *The great Atlantic Sargassum belt* (Science) | 1 |
| Mon 26 Oct | Self-directed reading: satellite imaging fundamentals (orbits, resolution/GSD, SAR) | 1.5 |
| Mon 26 Oct | Sentinel-2 MSI and constellation; NDVI and how vegetation reflects red/NIR | 1 |
| Mon 26 Oct | Research Notebook: background notes, Wang et al. entry, resolved one open question | 0.5 |
| Wed 28 Oct | RGB vs NIR analysis: identified the Sentinel-2 bands sargassum detection needs (B5–B8A) |0.5 |
| Wed 28 Oct | Read Hu (2009), Floating Algae Index; mapped it to Sentinel-2 bands (B4, B8A, B11) | 1.5 |
| Wed 28 Oct | Background research on generative models (autoencoder → VAE → GAN → diffusion) | 3 |
| Wed 28 Oct | Research Notebook: FAI section, generative-models notes, new open question on mixed band resolutions | 1 |
| Thu 29 Oct | Studied VAEs (latent space, mean/standard deviation, KL divergence) and how Stable Diffusion uses a VAE latent space | 1 |
| Thu 29 Oct | Reviewed the Research Notebook and prepared meeting talking points | 0.5 |
| Thu 29 Oct | Supervisor meeting with Dr Wei: multispectral, all 13 bands, higher-resolution option | 1 |
| Thu 29 Oct | Paired vs unpaired metrics: why PSNR/SSIM need a matching original image | 0.5 |

**Reflection:**
- Corrected my own misunderstanding: sargassum is detected by passive optical sensing (it reflects NIR strongly while water absorbs NIR), not by radar penetrating water.
- This directly affects the research design, because a standard RGB-only diffusion model would not produce the NIR signal that sargassum detection relies on.
- FAI explains why ocean studies avoid plain NDVI: a red–SWIR baseline cancels most of the haze and glint effect. This adds SWIR (B11) to the bands the synthetic images probably need.
- New design issue: the required bands come at mixed resolutions (10 m and 20 m).
- 29 Oct: Dr Wei's steer settles the RGB vs multispectral question: all 13 bands, because which bands matter most is something the experiments should show.

**Way forward:**
- Work with all 13 Sentinel-2 bands; for the mixed resolutions, focus on the higher-resolution option.

**Next steps:**
- Sentinel-2 band table (all bands, wavelengths, resolutions) for Dr Wei.
- Go through the links Dr Wei sent: the DiffusionSat paper (arXiv 2312.03606), project page and GitHub repository.

## Week 2 — w/c 2 Nov 2026 — Hours: _ ( Total so far: 26/225)

| Date | Task | Hours |
| --- | --- | --- |
| Mon 2 Nov | Paired vs unpaired metrics: why SSIM is paired too; FID (Heusel et al., 2017) as an unpaired distribution metric and its limits for 13-band data | 2 |
| Mon 2 Nov | Conditioned generation (super-resolution) as a way to create pairs; hallucination risk for sargassum | 1 |
| Mon 2 Nov | Research Notebook: updated the paired vs unpaired entry | 1 |
| Tue 3 Nov | Why Stable Diffusion's RGB-trained VAE can't handle 13-band Sentinel-2 input (input-layer mismatch; RGB-learned compression loses NIR contrast); NIR vs thermal infrared | 1 |
| Tue 3 Nov | Built the Sentinel-2 band table requested by Dr Wei (all 13 bands: wavelength, bandwidth, resolution, relevance to sargassum) from ESA SentiWiki, using S2B values with differences from S2A | 2 |
| Thu 5 Nov | Wang et al. (2019) limitations: MODIS pixel size, cloud gaps and compositing, proposed vs proven drivers | 1 |
| Thu 5 Nov | Sentinel-2 processing levels (L1C vs L2A): B10 dropped from L2A, only 4 native 10 m bands; proposed L2A | 1 |
| Thu 5 Nov | DiffusionSat first pass: problem, metadata conditioning, RGB-only output, metrics used | 1 |
| Thu 5 Nov | Prepared supervisor meeting talking points | 1 |
| Fri 6 Nov | Drafted progress summary and questions email to Dr Wei (meeting cancelled) | 0.2 |
| Fri 6 Nov | DiffusionSat method: metadata conditioning via sinusoidal embeddings; which metadata matters for sargassum; cloud cover idea for Phase 4 | 1.8 |

