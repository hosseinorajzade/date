# Daewoo Charisma 9Kg teaser (vertical)

1080x1920, 30 fps, H.264, 43 s, audio at -14 LUFS. Final file: `daewoo_teaser_final.mp4`.

## Pipeline

1. `scripts/prep.sh`: normalizes the Veo clips in `raw/` to 1080x1920/30 fps (center scale and crop) and applies the shared grade (deep blacks, contrast, saturated reds, light sharpening) into `prep/`.
2. Clip repairs (OpenCV):
   - `scripts/track_intro_logo.py` + `scripts/patch_intro_logo.py`: the panel logo in `01_intro` was AI-garbled ("DACIVOO"). It is tracked with optical flow, inpainted, and replaced with the real wordmark.
   - `scripts/blur_labels.py`: softens the fake panel words in `03_panel` (shots 3 and 4) with a tracked, feathered blur.
   - `scripts/machine_mask.py`: machine silhouette per frame, so "Charisma" sits behind the machine in shot 2.
   - `scripts/track_s3_logo.py`: logo box per frame for the neon outline in shot 3.
3. Segments in `remotion/public/clips/` are cut and retimed with ffmpeg. Shot 3 is a 0.4x motion-interpolated slow-mo. Shots 6, 7 and 9 are retimed slightly so their light changes land on the beat.
4. `remotion/src/timeline.json` is the single source of truth for cuts, titles, transitions and logo timing.
5. `scripts/make_audio.py` synthesizes the score (120 BPM, D minor) and the SFX from that timeline. `scripts/master_audio.sh` mixes and masters to -14 LUFS with true peak at or below -1 dBTP.
6. Remotion (`remotion/src/Teaser.tsx`) builds the picture: shots, transitions, Persian/English captions (Vazirmatn/Roboto, RTL), typing, logo ending.
7. `scripts/finalize_qc.sh`: muxes, then runs the QC (1 fps contact sheet, cuts vs beat grid, loudness).

Render:

```bash
cd remotion && npx remotion render src/index.ts Teaser out/teaser_video.mp4 --codec=h264 --crf=15 --muted \
  --browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
```

Large media (`raw/`, `prep/`, `work/`, rendered clips) is not committed.
