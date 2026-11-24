from pathlib import Path

from sigport.hgnc import HgncTables, load_hgnc
from sigport.resolve import GeneResolver

FIXTURES = Path(__file__).parent / "fixtures"
COMPLETE_SET = FIXTURES / "hgnc_subset.tsv"
WITHDRAWN = FIXTURES / "withdrawn_subset.tsv"


def _resolver() -> GeneResolver:
    tables = load_hgnc(COMPLETE_SET, WITHDRAWN)
    return GeneResolver(tables)


def test_resolve_exact():
    df = _resolver().resolve(["TP53"])
    row = df.iloc[0]
    assert row["category"] == "exact"
    assert row["hgnc_id"] == "HGNC:1002"
    assert row["approved_symbol"] == "TP53"


def test_resolve_previous():
    df = _resolver().resolve(["ORC6L", "CDCA1"])
    assert list(df["category"]) == ["previous", "previous"]
    assert list(df["approved_symbol"]) == ["ORC6", "NUF2"]


def test_resolve_alias():
    df = _resolver().resolve(["NUF2R", "HER2"])
    assert list(df["category"]) == ["alias", "alias"]
    assert list(df["approved_symbol"]) == ["NUF2", "ERBB2"]


def test_resolve_ambiguous_shared_alias():
    """DUPALIAS is listed as an alias of both GENEA and GENEB in the fixture."""
    df = _resolver().resolve(["DUPALIAS"])
    row = df.iloc[0]
    assert row["category"] == "ambiguous"
    assert row["hgnc_id"] is None
    assert row["candidates"] == "HGNC:1008|HGNC:1009"


def test_resolve_withdrawn():
    df = _resolver().resolve(["OLDGENE1"])
    assert df.iloc[0]["category"] == "withdrawn"
    assert df.iloc[0]["hgnc_id"] is None


def test_resolve_unresolved():
    df = _resolver().resolve(["FAKEGENE"])
    assert df.iloc[0]["category"] == "unresolved"


def test_resolve_ambiguous_approved_vs_alias():
    """An input that is one gene's approved symbol but also another gene's alias must be
    ambiguous, never picked as exact."""
    tables = HgncTables(
        approved={
            "FOO": {
                "hgnc_id": "HGNC:9001",
                "symbol": "FOO",
                "entrez_id": 1,
                "ensembl_gene_id": "ENSG1",
            },
            "BAR": {
                "hgnc_id": "HGNC:9002",
                "symbol": "BAR",
                "entrez_id": 2,
                "ensembl_gene_id": "ENSG2",
            },
        },
        previous={},
        alias={"FOO": ["HGNC:9002"]},
        withdrawn=set(),
    )
    df = GeneResolver(tables).resolve(["FOO"])
    row = df.iloc[0]
    assert row["category"] == "ambiguous"
    assert row["candidates"] == "HGNC:9001|HGNC:9002"


def test_resolve_all_six_categories_in_one_call():
    df = _resolver().resolve(["TP53", "ORC6L", "NUF2R", "DUPALIAS", "OLDGENE1", "FAKEGENE"])
    assert list(df["category"]) == [
        "exact",
        "previous",
        "alias",
        "ambiguous",
        "withdrawn",
        "unresolved",
    ]
