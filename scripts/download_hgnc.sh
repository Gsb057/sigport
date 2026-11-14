#!/usr/bin/env bash
# Downloads the frozen HGNC monthly snapshot (complete set + withdrawn list)
# into data/snapshots/ and records a sha256 for each file.
set -euo pipefail

SNAPSHOT_DATE="2026-10-06"
BASE_URL="https://storage.googleapis.com/public-download-files/hgnc/archive/archive/monthly/tsv"
OUT_DIR="data/snapshots"

mkdir -p "$OUT_DIR"

download() {
    local fname="$1"
    local url="${BASE_URL}/${fname}"
    local out="${OUT_DIR}/${fname}"

    curl -fsSL "$url" -o "$out"

    local hash
    hash=$(sha256sum "$out" | awk '{print $1}')
    echo "${hash}  ${fname}" > "${out}.sha256"

    echo "downloaded ${fname} (sha256=${hash})"
}

download "hgnc_complete_set_${SNAPSHOT_DATE}.txt"
download "withdrawn_${SNAPSHOT_DATE}.txt"
