# Daewoo — «۸ پیمان ما با مشتریان» · Instagram Reel

1080×1920 · 30 fps · 45 s · 120 BPM · H.264 High + original synthesized soundtrack (AAC 192k, −14 LUFS).

**Deliverable:** `out/daewoo-8-promises.mp4`

## Files
- `index.html` — the full animation: a single paused GSAP 3.12.5 timeline (`window.tl`). All text, timings and colors are in the `CONFIG` object at the top of the script.
- `render.mjs` — the frame-accurate renderer (headless Chromium → ffmpeg). Each frame is rendered with `tl.seek(frame/30)`, so the output is deterministic.

## Preview
```bash
npx serve .
```
Open `http://localhost:3000/index.html`. Keys: Space play/pause · ←/→ step one frame · S toggle the Instagram safe zone · H hide the control bar.
`?t=SECONDS` seeks to a time; `?render=1` shows a clean 1:1 stage.

## Render
```bash
npm install
node render.mjs                      # full MP4 → out/daewoo-8-promises.mp4
node render.mjs --stills 2,10,64     # PNG stills → out/stills/
node render.mjs --from 7 --to 14     # partial render
```
The renderer serves GSAP and Vazirmatn from `node_modules`, so it runs offline.

## Structure (seconds) — 120 BPM, 1 bar = 2 s
| Time | Beat |
|---|---|
| 0–2.9 | Hook: a red 8 draws itself on a deep hit — «بعد از خرید، چه کسی کنار شماست؟» |
| 2.9–6.0 | «پیمان ما با مشتریان» · تعهد · احترام · آرامش. The kick comes in; the 8 empties and rises to become the progress indicator |
| 6.0–38.0 | Eight promises, 4 s (2 bars) each. Each promise fills one red segment of the 8, landing on the beat with a bell note |
| 38.0–45.0 | The segments fly apart and regroup (lock on 39.0), the 8 turns 90° into ∞ (lands on 40.0) above Daewoo appliances — «پیمانی بی‌پایان» + logo |

## Placeholders to replace before publishing
- **The eight promises' copy** in `CONFIG.promises` (numbers, titles, details). These are illustrative and must be replaced with the official commitments.
- **Logo:** `<g id="logo">` in `index.html` (currently the text "DAEWOO").
- **Font:** Vazirmatn stands in for the brand Persian font.

## Sound design
`audio.py` (numpy only) synthesizes an original 120 BPM soundtrack from the cue sheet that `index.html` exposes (`window.audioCues()`, derived from `CONFIG`), so the sound stays in sync when the timings change. Noise is seeded, so the output is deterministic.
- **Groove:** a four-on-the-floor kick with sidechain pumping, claps on 2 and 4, offbeat hats, and an 8th-note bass.
- **Arpeggio:** 16th-note plucks through the chords. Its filter opens across the piece to build energy.
- **Harmony:** one chord per promise (D · Bm · G · A). The finale builds G → A and lands on a bright D when the ∞ appears.
- **Bells:** a bell note when each 8 segment fills. Across the 8 promises the notes climb from D5 to D6.
- **Risers:** noise swells into every downbeat and into the finale, panned right → left to match the RTL motion.
- **Sub impacts:** on the hook, on the lock, and on the ∞ landing.

To rebuild only the soundtrack and remux it into the existing MP4 (about 25 s):
```bash
node render.mjs --audio-only
```
Requires `python3` with `numpy`.
