# Supervisor Direction — Dr Hong Wei

**Running record of guidance and steers from my supervisor. Update after each meeting.**

---

## Core direction (as of Week 4, Oct 2026)

- **Data focus:** look specifically for **Sentinel-2** imagery and the **sargassum class**. (MARIDA is the leading candidate dataset.)
- **Generate my own dataset:** down the line, use the real Sentinel-2 sargassum data to generate AI images, then do my own analysis comparing synthetic vs real using image quality metrics that give insight.
- **Model choice:** a **Stable Diffusion (diffusion) model** is more effective than a **GAN** for this task — better quality and stability; GANs suffer mode collapse.
- **Bands (Week 4):** generate **multispectral** imagery with **all 13 Sentinel-2 bands**, not RGB, because we don't yet know which bands contribute most; experimentation should show that. For the mixed band resolutions, focus on the **higher-resolution option**.
- **Goal of the analysis:** not just run standard metrics, but identify metrics that reveal whether generated images are genuinely usable (spectral/geospatial accuracy), beyond visual similarity.

---

## My understanding (confirmed correct, with one clarification)

- Correct: Sentinel-2 + sargassum class; generate synthetic dataset; compare against real using insightful metrics; Stable Diffusion over GAN.
- Clarification: the real data isn't mapped one-to-one into generated images — it's used to **train / fine-tune / condition** a generative model, which then produces new synthetic images for assessment.

---

## Meeting log

*One entry per Thursday meeting.*

### Week 1 — Thu 8 Oct 2026
- *To fill in*

### Week 2 — Thu 15 Oct 2026
- *To fill in*

### Week 3 — Thu 22 Oct 2026
- Agreed the **Core direction** above (Sentinel-2 + sargassum, own synthetic dataset, diffusion over GAN, insight-giving metrics).
- Confirmed **My understanding**, with the clarification that real data trains/conditions the model rather than being mapped one-to-one.

### Week 4 — Thu 29 Oct 2026
- **Email (morning):** the log organisation looks good. List all Sentinel-2 bands with their wavelengths and resolutions in a table (can also go in my FYP report). Sent the DiffusionSat paper (arXiv 2312.03606) and project page as help for generating satellite images with Stable Diffusion. Placement total is 225 hours, split into weeks from 26 Oct 2026 to 26 Feb 2027, maximum 20 hours per week.
- **Meeting:** generate multispectral, not RGB, using all 13 bands, since we don't yet know which bands contribute more. For mixed resolutions, focus on the higher-resolution option (my reading: 10 m; to confirm at the next meeting).
- **Next steps agreed:** go through the links she sent, including the DiffusionSat GitHub repository.
