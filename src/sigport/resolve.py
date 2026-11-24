"""Resolves gene symbols against a frozen HGNC snapshot (see CLAUDE.md §4)."""

import logging

import pandas as pd

from sigport.hgnc import HgncTables

logger = logging.getLogger(__name__)

COLUMNS = [
    "input_symbol",
    "hgnc_id",
    "approved_symbol",
    "entrez_id",
    "ensembl_gene_id",
    "category",
    "candidates",
]


class GeneResolver:
    """Maps raw gene symbols to HGNC IDs, classifying each into one of six categories.

    exact: the input is the approved symbol of exactly one gene.
    previous: the input is a former symbol of exactly one gene.
    alias: the input is an alternative symbol of exactly one gene (and not an approved symbol).
    ambiguous: the input matches more than one gene (via approved/previous/alias combined) —
        all candidate HGNC IDs are reported, none is picked.
    withdrawn: the input is a withdrawn HGNC entry with no merged-into target.
    unresolved: the input is not found anywhere in the snapshot.
    """

    def __init__(self, tables: HgncTables):
        self.tables = tables
        self._by_id = {record["hgnc_id"]: record for record in tables.approved.values()}

    def resolve(self, symbols: list[str]) -> pd.DataFrame:
        rows = [self._resolve_one(raw) for raw in symbols]

        counts: dict[str, int] = {}
        for row in rows:
            counts[row["category"]] = counts.get(row["category"], 0) + 1
        logger.info("resolved %d symbols: %s", len(rows), counts)

        return pd.DataFrame(rows, columns=COLUMNS)

    def _resolve_one(self, raw_symbol: str) -> dict:
        symbol = raw_symbol.strip()

        approved_record = self.tables.approved.get(symbol)
        prev_ids = self.tables.previous.get(symbol, [])
        alias_ids = self.tables.alias.get(symbol, [])

        candidate_ids = set(prev_ids) | set(alias_ids)
        if approved_record is not None:
            candidate_ids.discard(approved_record["hgnc_id"])

        if approved_record is not None and candidate_ids:
            all_ids = {approved_record["hgnc_id"]} | candidate_ids
            return self._ambiguous_row(symbol, all_ids)

        if approved_record is not None:
            return self._resolved_row(symbol, approved_record["hgnc_id"], "exact")

        if len(candidate_ids) >= 2:
            return self._ambiguous_row(symbol, candidate_ids)

        if len(prev_ids) == 1:
            return self._resolved_row(symbol, prev_ids[0], "previous")

        if len(alias_ids) == 1:
            return self._resolved_row(symbol, alias_ids[0], "alias")

        if symbol in self.tables.withdrawn:
            return self._empty_row(symbol, "withdrawn")

        return self._empty_row(symbol, "unresolved")

    def _resolved_row(self, symbol: str, hgnc_id: str, category: str) -> dict:
        record = self._by_id[hgnc_id]
        return {
            "input_symbol": symbol,
            "hgnc_id": hgnc_id,
            "approved_symbol": record["symbol"],
            "entrez_id": record.get("entrez_id"),
            "ensembl_gene_id": record.get("ensembl_gene_id"),
            "category": category,
            "candidates": None,
        }

    def _ambiguous_row(self, symbol: str, candidate_ids: set[str]) -> dict:
        return {
            "input_symbol": symbol,
            "hgnc_id": None,
            "approved_symbol": None,
            "entrez_id": None,
            "ensembl_gene_id": None,
            "category": "ambiguous",
            "candidates": "|".join(sorted(candidate_ids)),
        }

    def _empty_row(self, symbol: str, category: str) -> dict:
        return {
            "input_symbol": symbol,
            "hgnc_id": None,
            "approved_symbol": None,
            "entrez_id": None,
            "ensembl_gene_id": None,
            "category": category,
            "candidates": None,
        }
