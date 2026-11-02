# AUREL — Radiance Serum · 30s · Editing Report

## Deliverables (`renders/`)

| File | Spec |
|---|---|
| `AUREL_RadianceSerum_30s_9x16_1080x1920.mp4` | **Primary master.** 1080×1920, 24 fps, 720 frames (30.000 s), H.264 High CRF 17, BT.709, AAC 320k stereo 48 kHz, −16 LUFS integrated / −1.5 dBTP |
| `AUREL_RadianceSerum_30s_9x16_1080x1920_CLEAN.mp4` | Same, without type |
| `AUREL_RadianceSerum_30s_16x9_1920x1080.mp4` | Website edit, 1920×1080 (see "16:9 adaptation") |
| `AUREL_RadianceSerum_30s_16x9_1920x1080_CLEAN.mp4` | Website edit, without type |
| `AUREL_packshot_9x16.png` / `_CLEAN.png` | Final packshot still, 1080×1920 |
| `AUREL_packshot_16x9.png` | Final packshot still, 1920×1080 |

24 fps was chosen because every source clip is native 24 fps.

## Source material

The brief calls for **six** clips. **Five** were supplied:

| # | File (renamed in `source/`) | Content | Length |
|---|---|---|---|
| 1 | `01_first_drop_dark_pipette.mp4` | Pipette and droplet, dark espresso light stripes | 10.0 s |
| 2 | `02_skin_in_light_macro.mp4` | Macro of cheek, light sweep | 6.0 s |
| 3 | `03_formula_light_pipette.mp4` | Pipette, droplet released, ivory backdrop | 8.0 s |
| 4 | `04_ritual_application.mp4` | Woman applying serum by a window | 8.0 s |
| 5 | `05_bottle_packshot.mp4` | AUREL bottle on a travertine plinth | 8.0 s |

Both *The Reveal* and *The Signature* are cut from clip 5. No scene was invented to fill the gap.

## Edit decision list (programme time @ 24 fps)

| Scene | Programme | Source in → out | Speed | Notes |
|---|---|---|---|---|
| 1 The First Drop | 00:00:00 – 00:04:00 | clip 1, 3.35 → 7.35 s | 100% | 12-frame fade from black. The drop swells on the pipette tip. |
| 2 Skin in Light | 00:04:00 – 00:08:08 | clip 2, 0.25 → 4.58 s | 100% | Match cut from the droplet's specular highlight to the cheek. Window light then sweeps across the skin. |
| 3 The Formula | 00:08:08 – 00:12:05 | clip 3, 5.04 → 8.00 s | 75% | Restrained slow motion, motion-interpolated. The drop separates at 00:10:00. |
| 4 The Ritual | 00:12:05 – 00:15:18 | clip 4, 0.00 → 3.54 s | 100% | Hand rises from the neck to the cheek. The last 8 frames lift toward window-light ivory. |
| 5 The Reveal | 00:15:18 – 00:24:12 | clip 5, 5.30 → 8.00 s | ≈30% | Opens on the same light lift (ritual-to-product transition by light). Slow hero push-in, motion-interpolated so the label stays crisp. |
| 6 The Signature | 00:24:00 – 00:30:00 | clip 5, frame 40 → frame 0 | eased ≈30% → 0 | 12-frame dissolve from the Reveal (the spot's only dissolve). Gentle settle-back that lands on the cleanest original frame of the bottle. Type fades in. |

Timecodes are HH:MM:SS:FF. All cuts are straight, apart from the opening fade and the single Reveal → Signature dissolve. No speed ramps, whooshes or social-style effects are used. The only reversed footage is the bottle shot, which has no liquid or hands in it, so the reversal can't be seen.

The scene lengths differ slightly from the brief (Ritual 3.5 s instead of 5 s, Reveal 8.25 s instead of 7 s). The Ritual clip is only clean for its first 3.5 s (see below). The extra time went to the Skin and Reveal shots rather than to flawed footage.

## Continuity and AI-artifact report

| Clip | Issue | Where | Handling | Recommendation |
|---|---|---|---|---|
| 1 First Drop | An artificial star or lens flare appears at the pipette tip | 7.5 s → end | Out-point at 7.35 s, before the flare | OK as cut |
| 1 First Drop | The drop disappears and recoils into the pipette without falling | ~9.7 s | Not used | — |
| 2 Skin | The image blows out into artificial bokeh and haze | 4.67 s → end | Out-point at 4.58 s | OK as cut |
| 3 Formula | Discontinuity: the liquid stream snaps and a new drop instantly appears on the tip | 4.75 – 5.0 s | In-point at 5.04 s, after the reset | OK as cut |
| 4 Ritual | **A translucent circular "disc" appears on the cheek** under the fingers and never fully clears; a faint ring stays to the end | 3.6 s → end | Out-point at 3.54 s. A tighter cut-in from later in the clip was tried and **rejected** because the ring is visible | **Regenerate or replace** this shot with a clean 5–6 s application take. That would restore the brief's 5 s Ritual. |
| 4 Ritual | Fingers look semi-transparent (ghosting) | ~5.3 – 5.8 s | Not used | — |
| 4 Ritual | A persistent bead of serum on the temple | whole clip | Kept (reads as a dab of product) | Optional clean-up in a replacement take |
| 5 Bottle | **The plinth briefly turns to water and ripples spread across the floor** | 2.4 – 5.2 s | Excluded. Reveal uses 5.30 s → end; Signature uses 0 → 1.67 s | OK as cut |
| 5 Bottle | Very small fine-print text (volume line) shimmers frame to frame | throughout | Too small to read at delivery size | Accept |

**Product continuity.** The AUREL bottle comes from one clip only (5), so its silhouette, cap, glass tint and label stay consistent wherever it appears. No bottle was altered, retouched or added.

The pipettes in clips 1 and 3 are generic glass droppers, not a matched AUREL pipette: one is in dark light, the other in ivory light. They read as the same product in different light. If the bottle's real dropper differs, regenerate clips 1 and 3 from the product reference image.

No product-reference image was supplied, so continuity was checked against clip 5.

**Packshot backdrop extension.** To fit the brand name above the product and the tagline below it inside platform-safe margins, the final shot is pulled back to 88%. The plain ivory wall and floor are continued into the new margin by edge extension. The product and plinth are untouched; only the empty seamless backdrop is extended.

## Color grade

All per-shot settings are in `scripts/config.py`, applied at source resolution and then upscaled with Lanczos (720p → 1080p), lightly sharpened, and given a fine shared grain so five differently generated clips share one texture.

- **First Drop:** rich espresso shadows with the black point lifted (0 → 0.025) so nothing crushes. Warm, not orange, shadows. Highlights roll off at 95%.
- **Skin:** the source runs orange and yellow. Mids and highlights were pulled toward natural skin and saturation reduced (−14%), with a soft highlight shoulder. No smoothing or beauty filter, so pores and texture stay intact.
- **Formula:** neutralized the yellow backdrop toward ivory (blue added in the highlights, −10% saturation).
- **Ritual:** the same skin treatment as Skin in Light, so she reads as the same person in the same light.
- **Reveal and Signature:** brightened toward a clean ivory (backdrop about RGB 233/229/219), neutral whites with a warm cast, champagne glass reflections left as shot.

The arc runs from dark espresso (0–4 s) to the bright ivory packshot (24–30 s).

## Sound (original, synthesized — no samples, no licensing exposure)

`scripts/soundtrack.py` generates every sound from scratch: detuned pads, an additive-synthesis piano, and synthesized water, glass, air and room textures, with a convolution reverb. It imitates no existing track. The mix is normalized to −16 LUFS with −1.5 dBTP true-peak headroom, a common web and social target. Measured integrated loudness is −15.9 LUFS.

| Time | Cue |
|---|---|
| 0.0 – 4.0 | Low sub atmosphere and a D maj9 pad (dark, swelling in); piano A4 |
| 0.85 | Faint glass "tink" as light catches the pipette |
| 3.88 | Delicate droplet sound, a bridge across the match cut |
| 4.0 – 8.3 | B minor colour and a gentle airy texture for the macro skin |
| 8.33 | Cut to the formula; glass detail |
| **10.00** | **Droplet "plip", synced to the drop separating from the pipette** |
| 12.2 – 15.75 | Quiet room tone, E minor 9; soft skin-touch texture at 13.75 when the fingertips meet the cheek |
| 15.75 | Hero reveal: soft low G accent (sub swell) and a low piano G/D; the rise begins (G maj9 → A sus4 crescendo, high shimmer joins) |
| 24.0 | Resolution to D add9 on the dissolve to the Signature; rolled piano chord |
| 25.0 / 26.4 | Piano A5 and D6, landing with the brand name and tagline |
| 27.8 – 30.0 | Natural decay and fade to near-silence |

## Typography

- **AUREL:** Cormorant Garamond Medium, 0.30 em tracking, in espresso ink (RGB 52/41/33), never pure black.
- **RADIANCE SERUM:** Inter Light, 0.42 em tracking.
- **Tagline** ("Your Skin, In Its Own Light."): Cormorant Garamond Regular.

The brand lockup fades in at 25.0 s and the tagline at 26.4 s, each with a plain one-second opacity fade and no per-letter animation. In the vertical master, the brand baseline sits at y = 346 (18%) and the tagline baseline at y = 1622 (84.5%). All text stays within 10% horizontal and 12% vertical margins, and nothing overlaps the product. Both fonts are under the SIL Open Font License, so commercial use is fine.

No claims, ingredients, results or before/after statements were added.

## 16:9 website adaptation

Every source is vertical (720×1280). A full-bleed 16:9 crop would mean upscaling about 4.7× from a 720×405 window, which isn't acceptable. Stretching is ruled out by the brief.

The website edit is an editorial split frame instead. Each shot is reframed separately to a 4:5 window (offsets in `CROP_Y_16x9`, `scripts/assemble.py`) and shown at 864×1080 on the right; this is actually a downscale from the 1080p grade, so it's sharper than the vertical master. A matched ivory panel on the left carries the typography. The cut, timing and sound are identical to the master.

If a full-bleed 16:9 hero is required, generate 16:9 versions of the clips from the same prompts and seeds and re-run the pipeline with `W, H = 1920, 1080`.

## Rebuild

```bash
cd aurel
python3 -I scripts/render_shots.py   # graded shots  -> build/*.mkv (FFV1, lossless)
python3 -I scripts/soundtrack.py     # score + SFX   -> build/soundtrack_f32.raw
python3 -I scripts/typography.py     # type overlays -> build/type_*.png
python3 -I scripts/assemble.py       # masters, clean versions, stills -> renders/
```

Requires ffmpeg ≥ 6 (with minterpolate and xfade), Python 3 with numpy and Pillow. A full rebuild takes about 15 minutes on 4 cores.
