#!/bin/bash
# Usage: tools/record_national_get.sh <url> [maxchars]  -> saves HTML to raw/record/national/web/<slug>.html and prints readable text
D=/home/user/Politicsnz/raw/record/national/web; mkdir -p $D
u="$1"; n="${2:-8000}"
f=$D/$(echo "$u" | sed 's#https\?://##; s#[^A-Za-z0-9._-]#_#g' | cut -c1-150).html
[ -s "$f" ] || curl -sSL --max-time 40 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/141 Safari/537.36" -o "$f" "$u"
python3 -I /home/user/Politicsnz/tools/record_national_text.py "$f" "$n"
