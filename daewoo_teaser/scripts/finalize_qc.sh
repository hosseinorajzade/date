#!/usr/bin/env bash
# Mux the rendered picture with the mastered audio, then run the QC checks:
# 1 frame/second contact sheet, detected cuts vs the 120 BPM grid, loudness/true peak, format.
set -euo pipefail
cd "$(dirname "$0")/.."
V=remotion/out/teaser_video.mp4
OUT=daewoo_teaser_final.mp4
ffmpeg -v error -y -i "$V" -i audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 \
  -movflags +faststart -shortest "$OUT"
echo "== format"; ffprobe -v error -show_entries stream=codec_name,profile,width,height,r_frame_rate,pix_fmt,sample_rate,channels -show_entries format=duration,size -of compact "$OUT"
echo "== loudness"; ffmpeg -hide_banner -i "$OUT" -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A20 Summary | grep -E "I:|Peak:"
echo "== cuts (scene > 0.25) vs beat grid"
ffmpeg -hide_banner -i "$OUT" -vf "select='gt(scene,0.25)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*" | cut -d: -f2 | \
  python3 -c "import sys; ts=[float(x) for x in sys.stdin]; [print(f'{t:7.3f}s  nearest beat {round(t*2)/2:5.1f}  off {abs(t-round(t*2)/2)*1000:5.0f} ms') for t in ts]"
mkdir -p review/qc
ffmpeg -v error -y -i "$OUT" -vf "fps=1,scale=240:-2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{eif\:t\:d}s':x=6:y=6:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.7,tile=11x4:padding=4:color=black" -frames:v 1 review/qc/contact_1fps.png
echo "sheet: review/qc/contact_1fps.png"
