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

## Week 5 — 2–8 Nov 2026 (in progress)

**Activities:**
- **Mon 2 Nov:**
    - Continued paired vs unpaired metrics. I'm looking for an unpaired metric, because my generated images won't have a direct real counterpart but I still need a way to judge their accuracy. SSIM compares luminance, contrast and structure, but still against a matching original, so it is paired like PSNR.
    - FID (Heusel et al., 2017): passes each image through Inception-v3 and compares the mean and covariance of the real and generated feature sets. It scores collections, not single images.
    - Super-resolution as conditioned generation: shrinking a real high-resolution image myself gives a known original to compare to, which makes PSNR/SSIM valid again.
- **Tue 3 Nov:**
    - Worked out what Stable Diffusion's RGB-trained VAE means for 13 bands. It can't take them at all: its first convolution expects 3 input channels. Even if forced, sargassum and water both look dark in RGB, so the VAE may pack them close together, but they are far apart in NIR, and its training never rewarded keeping that NIR contrast. A 13-band model needs a VAE retrained or fine-tuned on multispectral data.
    - Built the Sentinel-2 band table (Research Notebook) from ESA SentiWiki, S2 Mission: name, central wavelength, bandwidth and resolution for all 13 bands, plus relevance to sargassum. I used Sentinel-2B values (one of the two operational units) and noted each value's difference from 2A in brackets.
- **Thu 5 Nov:**
    - Wang et al. (2019) limitations: MODIS pixels are hundreds of metres wide, so isolated patches moving to shore may be missed; clouds block every optical band, so maps have to be composited over longer periods, losing timely detection; the drivers (Amazon discharge, West African upwelling) are proposed, not proven.
    - Sentinel-2 processing levels ([SentiWiki, S2 Products](https://sentiwiki.copernicus.eu/web/s2-products)): Level-1C is top-of-atmosphere reflectance with 13 bands; Level-2A is surface reflectance after atmospheric correction (made from L1C by Sen2Cor), with 12 bands. B10 is dropped because it sits in a strong water vapour absorption band and only sees high cirrus, not the surface. In L2A only B2, B3, B4 and B8 are native at 10 m.
    - DiffusionSat (Khanna et al., 2024) first pass: it conditions on metadata (location, GSD, cloud cover, date) instead of captions. It keeps Stable Diffusion 2.1's VAE, so its output is RGB only; multispectral data is used only as input for super-resolution. Its metrics (FID, IS, CLIP score, SSIM, PSNR, LPIPS) are all RGB and none check spectral accuracy.
- **Fri 6 Nov:**
    - DiffusionSat metadata conditioning: numbers can't go in the text prompt because the text encoder has no idea of numeric distance, so each value is turned into a sinusoidal embedding (like the timestep embedding), passed through its own MLP and added to the timestep embedding (Khanna et al., 2024, Appendix A.2).
    - Relevance: latitude/longitude and date matter most for sargassum (where and when it appears); GSD adds nothing if all images are Sentinel-2 at 10 m. Idea for Phase 4: use cloud cover to generate mostly clear images plus a realistic share of cloudy ones.

**Reflection:**
- I first named SSIM as the unpaired metric; it is paired. I also thought B4/B3/B2 were fed to FID because they matter most for sargassum, but they are used only because Inception was trained on RGB. The bands FAI relies on (red-edge/NIR) go unchecked.
- FID is limited rather than unviable: a set of synthetic images can score well on RGB statistics while its NIR/red-edge bands are wrong. It can serve as a baseline, which supports the case for domain-specific metrics in my report.
- 3 Nov: I confused NIR with thermal infrared. NIR is reflected sunlight just past red (B8 ≈ 0.84 µm); thermal is emitted heat (~8–14 µm), and Sentinel-2 has no thermal bands. Plants *reflect* NIR, they don't release it.
- Band table: the numbers were right, but my relevance column had mistakes. I marked bands as "no relevance" when they matter indirectly (B1, B9, B10 for atmospheric correction and cloud masking), missed that the red-edge bands (B5–B7) are the vegetation signal itself, copied land-only uses (urban, geology, soil), and mixed up the FAI bands (it uses B4, B8A, B11, not B12 or B8).
- 5 Nov: I'd prefer L2A because, across different dates and places, values reflect the surface more consistently, regardless of changing haze. A model trained on L1C would also learn to generate haze, and my metrics couldn't tell a haze mismatch from a sargassum mismatch. My first reason (L2A avoids compositing) was wrong: atmospheric correction doesn't remove thick cloud.
- 5 Nov: I predicted correctly that DiffusionSat outputs RGB, because it keeps an RGB-trained VAE. This conflicts with the steer to generate all 13 bands, so it's a decision for Dr Wei.
- 6 Nov: I mixed up cloud cover with haze. Haze is a thin layer that L2A corrects even on clear days; thick cloud hides the surface and L2A can only flag it. A detector trained only on cloud-free images may mistake cloud shadows for sargassum or miss sargassum under thin cloud.
- Super-resolution has two catches: my own downsampling isn't identical to a real low-resolution sensor, and a diffusion model can invent or erase small sargassum features without much effect on PSNR, because the scene is mostly water.

**Way forward:**
- Report FID as a baseline alongside domain-specific metrics, and consider a sargassum-specific check (e.g. FAI on the output) for super-resolved images.

**Next steps:**
- Thu 5 Nov supervisor meeting was cancelled because of a clashing departmental meeting. Dr Wei asked for a paragraph summarising my progress, with any questions by email.
- Raise with Dr Wei: L1C vs L2A, 10 m, and DiffusionSat's RGB-only output.
- Continue the DiffusionSat breakdown (method in detail, key results, limitations).

## Week 6 — 9–15 Nov 2026 (in progress)

**Activities:**
- **Mon 9 Nov:**
    - DiffusionSat image conditioning: to make the output follow a specific real scene, a corresponding image is input alongside the metadata. A ControlNet-style module (Zhang et al., 2023) trains a copy of the U-Net encoder on the guiding image while the original stays frozen. DiffusionSat's 3D version takes several images of the same place on different dates; it is order-invariant, but each image's date metadata still carries the timeline.
    - DiffusionSat results: on fMoW super-resolution (Table 2), DBPN wins PSNR and MSE while DiffusionSat wins SSIM and LPIPS; on Texas housing (Table 3), STSR wins SSIM and PSNR while DiffusionSat wins LPIPS. The authors note PSNR/SSIM favour blurriness over sharp detail.
- **Tue 10 Nov:**
    - Worked out why every model scores low on fMoW super-resolution: the resolution gap is larger (Sentinel-2 10–60 m to fMoW 0.3–1.5 m, dataset from Cong et al., 2022, vs 10× for Texas), and the Texas task also gets a high-resolution image of the same place at another time, so the model can copy the layout instead of inventing all the detail.
    - Dr Wei replied to my progress email: the three questions will be decided at the next meeting, and in general we should generate the same data format as Sentinel-2.
    - DiffusionSat limitations for my project: RGB-only output lacks the multispectral data needed for sargassum; none of its metrics check spectral accuracy; temporal generation can't predict wind-driven drift, so it can hallucinate patches in the wrong place.

**Reflection:**
- If Stable Diffusion were fully retrained on one narrow task, it may forget the general skills it learned before (catastrophic forgetting), and small paired datasets risk overfitting, which is why the original network is frozen.
- Multiple dates help because a clear date shows sargassum that a cloudy one hides, and a sequence shows where it is headed and whether its density is increasing. But generating a plausible future image is not the same as physically forecasting drift.
- I first read the wrong results table (Table 3 instead of Table 2) and wrote "highest LPIPS" when lower is better. The main takeaway: which model "wins" depends on the metric, because pixel-error metrics reward safe, blurry outputs. This is a direct argument for my project.

- I first thought the Texas model was peeking ahead and cheating; it isn't, that's the task design. Scores from different tasks aren't comparable, even with the same metric.
- My reading of Dr Wei's steer is multispectral output with Sentinel-2's bands and resolutions, which would mean DiffusionSat's RGB-only output isn't enough as it is. To confirm at the next meeting.

**Way forward:**
- Treat PSNR/SSIM with caution in my evaluation, and include a perceptual metric (e.g. LPIPS) alongside domain-specific ones.

**Next steps:**
- Check what limitations the DiffusionSat authors themselves admit, and look at the GitHub repository.
- Process Dr Wei's reply to my progress email.

