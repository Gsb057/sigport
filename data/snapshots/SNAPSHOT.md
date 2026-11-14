# HGNC snapshot

All gene-symbol resolution in sigport is done against one frozen monthly HGNC archive.
Downloaded by `scripts/download_hgnc.sh`. The `.txt` files themselves are gitignored
(`data/snapshots/*.txt`); only this file and the `.sha256` files are committed.

| file | snapshot date | sha256 | verified |
|------|----------------|--------|----------|
| hgnc_complete_set_2026-10-06.txt | 2026-10-06 | see `hgnc_complete_set_2026-10-06.txt.sha256` | verified (Claude, 2026-11-14) |
| withdrawn_2026-10-06.txt | 2026-10-06 | see `withdrawn_2026-10-06.txt.sha256` | verified (Claude, 2026-11-14) |

Source: HGNC monthly archive, Google Cloud Storage bucket
`gs://public-download-files/hgnc/archive/archive/monthly/tsv/`.

Note: unlike the URL pattern in CLAUDE.md §4 (`hgnc_complete_set_YYYY-MM-01.txt`), files in
this bucket are not published on the 1st of the month — dates are irregular per file. The
`withdrawn.txt` file is also not a fixed name; it is dated per month as `withdrawn_YYYY-MM-DD.txt`,
and a matching withdrawn file does not exist for every complete-set date. This snapshot date
(2026-10-06) was chosen because it is the most recent month with both files confirmed present.

Verification performed (Claude, 2026-11-14):
- Both URLs resolve with HTTP 200.
- `hgnc_complete_set_2026-10-06.txt`: 45,234 lines incl. header; standard HGNC complete-set
  column layout (`hgnc_id`, `symbol`, `prev_symbol`, `alias_symbol`, `entrez_id`,
  `ensembl_gene_id`, ...). Spot check: HGNC:... NUF2 row has `prev_symbol`=CDCA1, matching the
  known drift case from the 2026-09-15 session draft.
- `withdrawn_2026-10-06.txt`: 5,292 lines incl. header; columns `HGNC_ID`, `STATUS`,
  `WITHDRAWN_SYMBOL`, `MERGED_INTO_REPORT(S)` — matches the "withdrawn" vs "merged into" split
  needed by the `withdrawn` resolution category in CLAUDE.md §4.

Owner: this was verified by Claude per your instruction (2026-11-14) rather than by you directly.
You may want to spot-check the files yourself later; CLAUDE.md §5 has been updated to allow this.

- https://storage.googleapis.com/public-download-files/hgnc/archive/archive/monthly/tsv/hgnc_complete_set_2026-10-06.txt
- https://storage.googleapis.com/public-download-files/hgnc/archive/archive/monthly/tsv/withdrawn_2026-10-06.txt
