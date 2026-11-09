#!/bin/bash
# Usage: tools/tighten_voice.sh in.mp3 out.mp3
# Shortens every silence longer than 0.30 s down to 0.22 s and normalises loudness.
set -e
ffmpeg -v error -y -i "$1" -af "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.3:stop_threshold=-45dB:stop_silence=0.22,loudnorm=I=-16:TP=-1.5:LRA=11" -ar 44100 -b:a 192k "$2"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$2"
