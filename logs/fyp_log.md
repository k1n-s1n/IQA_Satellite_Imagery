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

## Week 4 — 26 Oct – 1 Nov 2026 (in progress)

**Activities:**
- **Mon 26 Oct:**
    - Read Wang et al. (2019), *The great Atlantic Sargassum belt* (Science): since 2011 a recurring sargassum belt has stretched from West Africa to the Gulf of Mexico (about 8,850 km long, over 20 million tonnes in June 2018), mapped from about 19 years of MODIS data. This gives my report its motivation for satellite-based sargassum monitoring.
    - Self-directed reading on how satellite imagery works: orbits (LEO, geostationary, sun-synchronous), revisit time and constellations, resolution (GSD), and SAR/InSAR.
    - Sentinel-2 specifics: its MultiSpectral Instrument (MSI) is a passive optical push-broom sensor; constellation status (2A, 2B, 2C).
    - NDVI and how vegetation reflects light: plants absorb red and reflect near-infrared (NIR).
- **Wed 28 Oct:**
    - Answered my RGB-vs-NIR question: an RGB-only image contains no NIR information at all, so a synthetic RGB image could score well on PSNR/SSIM yet lack the signal sargassum detection depends on. Identified the red-edge (B5–B7) and NIR (B8, B8A) bands as needed.
    - Read Hu (2009), *A novel ocean color index to detect floating algae in the global oceans* (Remote Sensing of Environment): the Floating Algae Index (FAI) is NIR reflectance minus a linear red–SWIR baseline, which makes it less sensitive to haze, aerosols and sun glint than NDVI. Mapped it to Sentinel-2 bands B4, B8A and B11.
    - Background reading on generative models (autoencoder → VAE → GAN → diffusion), from IBM, Wikipedia, Medium and GeeksforGeeks articles and the YouTube video *AutoEncoder to Diffusion (For Beginners)*.
- **Thu 29 Oct:**
    - Worked through VAEs step by step. In my own words: a plain autoencoder's encoder takes an image and produces a fixed latent code *z*, one exact point in latent space, and the decoder rebuilds the image from it. Random points between those codes were never trained on, so decoding them gives garbage. A VAE's encoder instead outputs a mean and a standard deviation, and *z* is sampled from them, so nearby points learn to decode to similar images. Reconstruction alone pushes the standard deviation towards 0, so a KL divergence term pulls each image's distribution towards a standard normal N(0, 1) (mean to 0, standard deviation to 1). The tug of war between the two loss terms keeps the latent space both accurate and continuous (Kingma & Welling, 2013).
    - Introduced to how Stable Diffusion uses a VAE: diffusion runs in the compressed latent space and the decoder turns the result into an image (Rombach et al., 2022). Its VAE was trained on 3-channel RGB images.
    - Supervisor meeting with Dr Wei (details in `docs/supervisor_direction.md`): generate multispectral rather than RGB, using all 13 bands; focus on the higher-resolution option for the mixed band resolutions.

**Reflection:**
- My first hypothesis was that sargassum is detected with SAR "seeing through" water. That was wrong: Sentinel-2 is passive optical, and sargassum floats on the surface. It stands out because it reflects NIR strongly while water absorbs NIR.
- This changes how I see my RGB vs multispectral open question: the key sargassum signal is in NIR, which a standard RGB-only diffusion model would not generate.
- FAI: my first explanation of the baseline was wrong (I thought it removed clutter like water vapour and cirrus). Working through a toy example showed me it estimates the water + atmosphere background at NIR and subtracts it.
- Sargassum detection also relies on SWIR, and the bands I need come at mixed resolutions (10 m and 20 m). I logged this as a new open question.
- My generative-models summary leans heavily on one video transcript, and I had merged mode collapse with vanishing gradients. I need to cite the original papers (Kingma & Welling 2013; Goodfellow et al. 2014; Sohl-Dickstein et al. 2015; Ho et al. 2020; Rombach et al. 2022). VAEs hadn't clicked for me yet on 28 Oct.
- 29 Oct: VAEs now make sense to me; I was able to explain why a VAE can generate new images and a plain autoencoder can't. I need to watch my wording: the encoder *produces* the latent code, it doesn't compress "using" it.
- I didn't understand the paired vs unpaired metrics question well enough to raise it in the meeting. Afterwards I worked through it: PSNR is a paired metric, so it needs an original image of the same scene, and newly generated images don't have one. I'll continue with what this means for my metric choice next session.

**Way forward:**
- Generate all 13 Sentinel-2 bands, because we don't yet know which bands contribute most; experimentation should show that.
- For the mixed resolutions, focus on the higher-resolution option. I'm working with 10 m for now and will confirm with Dr Wei at the next meeting.

**Next steps:**
- Build a table of all Sentinel-2 bands with wavelengths and resolutions from the ESA MSI User Guide (requested by Dr Wei; also for my FYP report).
- Read and break down DiffusionSat (arXiv 2312.03606), go through the links Dr Wei sent, including the DiffusionSat GitHub repository.
- Continue the paired vs unpaired metrics question (distribution metrics such as FID vs conditioned generation that creates pairs).
