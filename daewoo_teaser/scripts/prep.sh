#!/usr/bin/env bash
# Stage 1: normalize every clip to 1080x1920 / 30fps (centre scale+crop, no stretching) and apply the unified grade:
# deep blacks (curves), extra contrast, saturated reds/magentas, light sharpening.
set -euo pipefail
cd "$(dirname "$0")/.."
GRADE="scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,curves=master='0/0 0.07/0.0 0.25/0.19 0.5/0.5 0.78/0.84 1/1',eq=contrast=1.06:saturation=1.08,huesaturation=saturation=0.28:colors=r+m:strength=6,unsharp=5:5:0.55:5:5:0,format=yuv420p"
mkdir -p prep
for f in raw/*.mp4; do
  n=$(basename "$f" .mp4)
  ffmpeg -v error -y -i "$f" -an -vf "$GRADE" -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -r 30 "prep/$n.mp4" &
done
wait
