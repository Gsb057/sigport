"""Readers for sigport. All file I/O for the library lives here (see CLAUDE.md §3)."""

import hashlib
import logging
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def _sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_table(
    path: str | Path,
    expected_rows: int | None = None,
    **read_csv_kwargs: object,
) -> tuple[pd.DataFrame, dict]:
    """Read a TSV file into a DataFrame, with row-count and hash checks.

    Args:
        path: path to the TSV file.
        expected_rows: if given, the read is expected to produce exactly this many data
            rows; a mismatch raises instead of silently returning a truncated/extended
            table (this is the check that would have caught the 4,213-vs-30,865-row
            truncated-read bug).
        **read_csv_kwargs: forwarded to `pandas.read_csv` (default separator is "\\t").

    Returns:
        (df, meta) where meta has keys: path, sha256, n_rows, n_cols, read_at.
    """
    path = Path(path)
    read_csv_kwargs.setdefault("sep", "\t")
    df = pd.read_csv(path, **read_csv_kwargs)

    n_rows, n_cols = df.shape
    if n_rows == 0:
        raise ValueError(f"read_table: {path} produced 0 rows")

    if expected_rows is not None and n_rows != expected_rows:
        raise ValueError(
            f"read_table: {path} produced {n_rows} rows, expected {expected_rows} "
            "(possible truncated read)"
        )

    meta = {
        "path": str(path),
        "sha256": _sha256_of(path),
        "n_rows": n_rows,
        "n_cols": n_cols,
        "read_at": datetime.now(UTC).isoformat(),
    }
    logger.info("read %d rows, %d cols from %s", n_rows, n_cols, path)
    return df, meta
