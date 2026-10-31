# Daewoo — «۸ پیمان ما با مشتریان» · Instagram Reel

1080×1920 · 30 fps · 68.5 s · H.264 High + original synthesized soundtrack (AAC 192k, −14 LUFS).

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

## Structure (seconds)
| Time | Beat |
|---|---|
| 0–3.7 | Hook: a red ۸ draws itself — «بعد از خرید، چه کسی کنار شماست؟» |
| 3.9–7.6 | «پیمان ما با مشتریان» · تعهد · احترام · آرامش. The ۸ empties and rises to become the progress roof |
| 7.6–58.8 | Eight promises at 6.4 s each. Each one fills one red segment of the ۸ |
| 58.8–68.5 | The segments fly apart and regroup, the ۸ becomes the roof of a home with Daewoo appliances — «۸ پیمان، یک سقف آرامش» + logo |

## Placeholders to replace before publishing
- **The eight promises' copy** in `CONFIG.promises` (numbers, titles, details). These are illustrative and must be replaced with the official commitments.
- **Logo:** `<g id="logo">` in `index.html` (currently the text "DAEWOO").
- **Font:** Vazirmatn stands in for the brand Persian font.

## Sound design
`audio.py` (numpy only) synthesizes an original soundtrack from the cue sheet that `index.html` exposes (`window.audioCues()`, derived from `CONFIG`), so the sound stays in sync when the timings change. Noise is seeded, so the output is deterministic.
- A warm pad in D major, one chord per promise (D · Bm · G · A), resolving to a bright D on the final roof.
- A bell note when each ۸ segment fills. Across the 8 promises the notes climb from D5 to D6.
- Soft ticks under the counters, and an airy swell under the word heroes.
- Noise whooshes on transitions, panned right → left to match the RTL motion.
- Deep sub impacts on the hook and when the roof locks into place.

To rebuild only the soundtrack and remux it into the existing MP4 (about 25 s):
```bash
node render.mjs --audio-only
```
Requires `python3` with `numpy`.
