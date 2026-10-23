#!/bin/bash
# Usage: tools/policies_nzf_tpm_fetch.sh <party-slug> <outname> <url>
# Downloads a source document into raw/party-docs/<party>/<outname> (NZ First / Te Pāti Māori policy research).
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36"
out="raw/party-docs/$1/$2"
curl -sS -L -A "$UA" --max-time 60 -o "$out" -w "%{http_code} %{size_download} $3\n" "$3"
