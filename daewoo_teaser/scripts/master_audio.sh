#!/usr/bin/env bash
# Mix music+SFX, glue-compress, then gain + 4x-oversampled limiter to land on -14 LUFS with true peak <= -1 dBTP.
set -euo pipefail
cd "$(dirname "$0")/../audio"
GAIN_DB=${1:-1.3}
ffmpeg -v error -y -i music.wav -i sfx.wav -filter_complex "[0]volume=1.0[m];[1]volume=0.62[s];[m][s]amix=inputs=2:normalize=0,acompressor=threshold=-16dB:ratio=2.5:attack=15:release=180:makeup=2,volume=${GAIN_DB}dB,aresample=192000,alimiter=limit=0.78:attack=2:release=80:level=disabled,aresample=48000" -c:a pcm_f32le master.wav
ffmpeg -hide_banner -i master.wav -af ebur128=peak=true -f null - 2>&1 | grep -A12 "Summary" | grep -E "I:|Peak:|LRA:"
