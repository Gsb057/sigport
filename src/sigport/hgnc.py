"""Loads one frozen HGNC snapshot into lookup tables used by gene-symbol resolution."""

import logging
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from sigport.io import read_table

logger = logging.getLogger(__name__)


@dataclass
class HgncTables:
    """Lookup tables built from one HGNC snapshot.

    approved: approved symbol -> record (hgnc_id, symbol, entrez_id, ensembl_gene_id)
    previous: previous symbol -> list of hgnc_ids of genes that once used it (>1 = ambiguous)
    alias: alias symbol -> list of hgnc_ids of genes that list it as an alias (>1 = ambiguous)
    withdrawn: set of withdrawn symbols with no resolution attempted here
    """

    approved: dict[str, dict]
    previous: dict[str, list[str]]
    alias: dict[str, list[str]]
    withdrawn: set[str]


def _split_multi(value: object) -> list[str]:
    if pd.isna(value) or value == "":
        return []
    return [s.strip() for s in str(value).split("|") if s.strip()]


def load_hgnc(complete_set_path: str | Path, withdrawn_path: str | Path) -> HgncTables:
    """Build HGNC lookup tables from a complete-set file and a withdrawn-symbols file."""
    complete_df, complete_meta = read_table(complete_set_path)
    withdrawn_df, withdrawn_meta = read_table(withdrawn_path)

    approved: dict[str, dict] = {}
    previous: dict[str, list[str]] = {}
    alias: dict[str, list[str]] = {}

    for record in complete_df.to_dict("records"):
        hgnc_id = str(record["hgnc_id"]).strip()
        symbol = str(record["symbol"]).strip()

        approved[symbol] = {
            "hgnc_id": hgnc_id,
            "symbol": symbol,
            "entrez_id": record.get("entrez_id"),
            "ensembl_gene_id": record.get("ensembl_gene_id"),
        }
        for prev_symbol in _split_multi(record.get("prev_symbol")):
            previous.setdefault(prev_symbol, []).append(hgnc_id)
        for alias_symbol in _split_multi(record.get("alias_symbol")):
            alias.setdefault(alias_symbol, []).append(hgnc_id)

    withdrawn = {
        s.strip()
        for s in withdrawn_df["WITHDRAWN_SYMBOL"].dropna().astype(str)
        if s.strip()
    }

    logger.info(
        "built HGNC tables from %s (%d rows) and %s (%d rows): "
        "%d approved, %d previous-symbol keys, %d alias keys, %d withdrawn",
        complete_meta["path"],
        complete_meta["n_rows"],
        withdrawn_meta["path"],
        withdrawn_meta["n_rows"],
        len(approved),
        len(previous),
        len(alias),
        len(withdrawn),
    )
    return HgncTables(approved=approved, previous=previous, alias=alias, withdrawn=withdrawn)
