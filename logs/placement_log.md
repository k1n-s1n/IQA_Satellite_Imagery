# Placement Log — Crocus / AI-INTERVENE

Research tasks, supervisor meetings and outputs. Target: 20 documented hours per week (26 Oct 2026 – 26 Feb 2027).

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

### Week 1 — 6–11 Oct 2026 — Hours (estimate):

**Activities:**
- General background research in the field of satellite imagery, getting familiar with the topic.

**Reflection:**
- Getting oriented in a field that is new to me.

**Way forward:**
- Narrow the reading towards the applied case.

**Next steps:**
- Read further into sargassum and how it is monitored.

### Week 2 — 12–18 Oct 2026 — Hours (estimate):

**Activities:**
- Further reading on sargassum in the open sea and how it is monitored with satellite imagery.

**Reflection:**
- I don't fully understand all of it yet and need a simpler breakdown of the remote-sensing side.

**Way forward:**
- Revisit the sargassum material once I'm more comfortable with spectral bands.

**Next steps:**
- Look at accessible datasets and the standard image quality metrics.

### Week 3 — 19–25 Oct 2026 — Hours (estimate):

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
