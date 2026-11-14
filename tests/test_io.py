from pathlib import Path

import pytest

from sigport.io import read_table

FIXTURE = Path(__file__).parent / "fixtures" / "sample_table.tsv"


def test_read_table_returns_df_and_meta():
    df, meta = read_table(FIXTURE)

    assert list(df.columns) == ["symbol", "value"]
    assert meta["n_rows"] == 5
    assert meta["n_cols"] == 2
    assert meta["path"] == str(FIXTURE)
    assert len(meta["sha256"]) == 64
    assert "read_at" in meta


def test_read_table_matching_expected_rows_passes():
    df, meta = read_table(FIXTURE, expected_rows=5)
    assert meta["n_rows"] == 5


def test_read_table_raises_on_row_count_mismatch():
    """Simulates a truncated read: the fixture has 5 data rows but the caller expected 10."""
    with pytest.raises(ValueError, match="produced 5 rows, expected 10"):
        read_table(FIXTURE, expected_rows=10)
