# FYP Log — CS3IP

Academic progress, deliverables and report-relevant decisions.
Detailed research notes live in the Research Notebook; this log stays short.

<!-- Entry template (newest at the bottom)
## Week N — DD Mon YYYY
**Activities:**
-
**Reflection:** (what went well, issues/challenges)
-
**Way forward:**
-
**Next steps:**
-
-->

## Week 1 — 6–11 Oct 2026

**Activities:**
- General background research in the field of satellite imagery, getting familiar with the topic.
- Completed and submitted the PID (8 Oct 2026).

**Reflection:**
- Getting oriented in a field that is new to me.

**Way forward:**
- Narrow the reading towards the applied case.

**Next steps:**
- Read further into sargassum and how it is monitored.

## Week 2 — 12–18 Oct 2026

**Activities:**
- Further reading on sargassum in the open sea and how it is monitored with satellite imagery.

**Reflection:**
- I don't fully understand all of it yet and need a simpler breakdown of the remote-sensing side.

**Way forward:**
- Revisit the sargassum material once I'm more comfortable with spectral bands.

**Next steps:**
- Look at accessible datasets and the standard image quality metrics.

## Week 3 — 19–25 Oct 2026

**Activities:**
- **Datasets researched:**
    - *Copernicus Data Space Ecosystem / Sentinel-2:* the primary source of real Sentinel-2 multispectral imagery, i.e. my real "ground truth" data. Free but large, so I need to understand how it is accessed.
    - *MARIDA (Marine Debris Archive):* a Sentinel-2-based benchmark that includes a Sargassum class alongside other marine features. Probably the most directly relevant dataset to my applied case.
- **Intro to key image quality metrics:**
    - *PSNR (Peak Signal-to-Noise Ratio):* measures pixel-level difference between two images (based on mean squared error), in decibels; higher means closer to the reference. Simple and fast, but it only looks at raw pixel values: it doesn't reflect how a human or a downstream model perceives the image, and it ignores spectral/geospatial meaning.
    - *SSIM (Structural Similarity Index):* compares images on luminance, contrast and structure rather than raw pixels, so it aligns better with perceived quality. Still a 2D, greyscale-oriented measure not designed for multispectral satellite data, so it misses spectral accuracy.
- **Thu 22 Oct, supervisor meeting with Dr Wei** (full notes in `docs/supervisor_direction.md`):
    - Focus specifically on Sentinel-2 imagery and the sargassum class.
    - Down the line, generate my own dataset: use the real data to train/condition a generative model, generate AI images, and compare them with real ones using image quality metrics that give real insight.
    - A Stable Diffusion (diffusion) model is more effective than a GAN for this task.
- **Repo and workflow setup:**
    - Moved the repo out of OneDrive to a local folder; raw datasets will stay in OneDrive.
    - Linked my personal GitHub as a second remote and overwrote its placeholder README with the GitLab history, so both mirrors are identical.
    - Set up an `all` remote so one `git push all main` updates GitLab and GitHub.
    - Added the repo skeleton: `.gitignore`, `README.md`, `data/README.md` (MARIDA listed as candidate dataset), log templates; moved supervisor docs into `docs/`.
    - Started a Research Notebook for paper breakdowns, open questions and decisions.

**Reflection:**
- Early insight on the metrics (still needs more reading): both were built for natural images and judge visual similarity. Neither accounts for spectral consistency (are the wavelength bands physically accurate?) or geospatial integrity. That gap is what my domain-specific measures aim to fill.
- After the meeting I have a clearer picture of what the research role wants from me and which direction to head.
- Moved from VS Code's Source Control panel to git on the command line: remotes, fetch, unrelated histories, force push, `.gitignore` rules.
- Issue: renaming the remote failed to clean up old files (Windows file lock), and my first clean-up attempt failed because I was in PowerShell, not Git Bash. Resolved; now using Git Bash.

**Way forward:**
- Two open questions logged in the notebook: paired vs unpaired metrics, and RGB vs multispectral generation.

**Next steps:**
- Read and break down DiffusionSat in the notebook.
- Fill in Week 1–2 supervisor feedback in `docs/supervisor_direction.md`.
- Confirm the markdown logbook format with Dr Wei on Thursday.
