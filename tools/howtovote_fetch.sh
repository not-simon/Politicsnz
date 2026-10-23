#!/bin/bash
# Fetch Electoral Commission pages (vote.nz / elections.nz block plain downloads) with the headless browser.
# Usage: tools/howtovote_fetch.sh <listfile>   where each line is "<url> <name>"; output raw/howtovote/<name>.html
# Pages already fetched are skipped.
cd "$(dirname "$0")/.." || exit 1
export NODE_PATH=/opt/node22/lib/node_modules
mkdir -p raw/howtovote
while read -r url name; do
  [ -z "$url" ] && continue
  out="raw/howtovote/$name.html"
  if [ -s "$out" ]; then echo "skip $name"; continue; fi
  timeout 100 node tools/fetch_page.js "$url" "$out" 2>&1 | grep -E 'TITLE|ERR' | sed "s/^/$name: /"
done < "$1"
