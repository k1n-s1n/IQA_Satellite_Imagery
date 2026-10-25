# Research Project Summary

**Reference document for the FYP / AI Research Intern project — background and direction.**

---

## Role & setup

- **Role:** AI Research Intern (Crocus / AI-INTERVENE placement), University of Reading, supervised by Dr Hong Wei.
- **Duration:** October 2026 onward.
- **Combined with:** my 3rd-year Computer Science Final Year Project (FYP). Same work, assessed on both tracks.
- **Title:** Image Quality Assessment for AI-Generated Satellite Imagery.

---

## The problem

Satellite imagery is used to monitor ocean sargassum, but training detection/segmentation models needs more labelled data than exists. One fix is generating **synthetic** satellite images with AI to augment the dataset.

The challenge: how do you know whether those generated images are actually **realistic and scientifically usable**? Standard image quality metrics (PSNR, SSIM) only judge visual/pixel similarity — they ignore the **spectral** and **geospatial** accuracy that remote sensing requires.

---

## The aim

Build a benchmarking pipeline that:

1. Generates synthetic Sentinel-2 sargassum imagery.
2. Evaluates it against real data.
3. Uses metrics that give genuine scientific insight — not just visual similarity — including domain-specific ones (spectral consistency, spatial frequency analysis, edge integrity).

---

## Direction (confirmed with supervisor)

- Focus on **Sentinel-2 data** and the **sargassum class** specifically. MARIDA (Marine Debris Archive) is the key starting dataset.
- **Generate my own dataset** down the line: use the real imagery to train/fine-tune/condition a generative model, produce synthetic images, then compare synthetic vs real.
- Use a **Stable Diffusion (diffusion) model** rather than a GAN — diffusion gives higher-quality, more stable, more diverse results; GANs suffer training instability and mode collapse.
- Core question throughout: **which metrics actually tell you if generated images are usable.**
- Anchor paper: **DiffusionSat** (Khanna et al., 2024) — a generative foundation model for satellite imagery, built on Stable Diffusion.

---

## Phases

1. **Literature review** — image quality metrics (PSNR, SSIM, and why they fall short for remote sensing) and generative models for imagery (diffusion-based).
2. **Setup** — dataset selection, generative model selection, programming environment.
3. **Domain-specific assessment** — spectral consistency, spatial frequency analysis, edge integrity.
4. **Downstream task** — sargassum segmentation to test whether synthetic images are useful for data augmentation.
5. **Reporting & demonstration.**

---

## Key terms

- **Mode collapse** — a GAN weakness where the model produces limited, repetitive outputs; a key reason diffusion is preferred.
- **Fine-tuning / conditioning** — adapting a pretrained Stable Diffusion model to produce sargassum/Sentinel-2-style images, rather than training from scratch (which needs huge compute).
- **Spectral consistency** — whether the generated image's wavelength bands are physically accurate, not just visually plausible.

---

## Metrics — quick reference

- **PSNR** — pixel-level difference (via MSE), in decibels; higher = closer. Fast, but ignores perception and spectral/geospatial meaning.
- **SSIM** — compares luminance, contrast and structure; closer to perceived quality, but 2D/greyscale-oriented and not designed for multispectral data.
- **FID** — standard generative-quality metric; compares feature distributions of real vs generated via a pretrained network. Features come from natural photos, not satellite imagery — a domain limitation.
- **LPIPS** — deep-feature perceptual similarity; closer to human judgement, but again trained on natural images.

**The through-line:** all of these were built for natural images and judge visual similarity. None account for spectral consistency or geospatial integrity — which is exactly the gap this project's domain-specific measures aim to fill.
