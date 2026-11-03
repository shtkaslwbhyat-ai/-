#!/usr/bin/env bash
# Usage: scripts/prepare-videogen-voice.sh s1.mp3 s2.mp3 ... s6.mp3
# Speeds each ElevenLabs clip up, removes every pause longer than a breath, evens the
# loudness, and writes public/videogen/s1.mp3 … s6.mp3 for the VideoGenTikTok composition.
set -euo pipefail
SPEED="${SPEED:-1.12}"
out="$(dirname "$0")/../public/videogen"
mkdir -p "$out"
i=1
for f in "$@"; do
  ffmpeg -y -loglevel error -i "$f" -af "\
silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.02,\
silenceremove=stop_periods=-1:stop_threshold=-40dB:stop_duration=0.12:stop_silence=0.06,\
atempo=${SPEED},\
acompressor=threshold=-24dB:ratio=3:attack=5:release=120:makeup=6dB,\
loudnorm=I=-14:TP=-1:LRA=7" -ar 44100 -b:a 192k "$out/s$i.mp3"
  printf 's%d: %ss\n' "$i" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$out/s$i.mp3")"
  i=$((i + 1))
done
