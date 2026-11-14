from pathlib import Path

from sigport.hgnc import load_hgnc

FIXTURES = Path(__file__).parent / "fixtures"
COMPLETE_SET = FIXTURES / "hgnc_subset.tsv"
WITHDRAWN = FIXTURES / "withdrawn_subset.tsv"


def test_load_hgnc_approved_table():
    tables = load_hgnc(COMPLETE_SET, WITHDRAWN)

    assert len(tables.approved) == 12
    assert tables.approved["ORC6"]["hgnc_id"] == "HGNC:1000"
    assert tables.approved["TP53"]["entrez_id"] == 7157


def test_load_hgnc_previous_symbol_table():
    tables = load_hgnc(COMPLETE_SET, WITHDRAWN)

    assert tables.previous["ORC6L"] == ["HGNC:1000"]
    assert tables.previous["CDCA1"] == ["HGNC:1001"]
    assert tables.previous["OLDD"] == ["HGNC:1011"]


def test_load_hgnc_alias_table():
    tables = load_hgnc(COMPLETE_SET, WITHDRAWN)

    assert tables.alias["NUF2R"] == ["HGNC:1001"]
    assert tables.alias["HER2"] == ["HGNC:1006"]


def test_load_hgnc_ambiguous_alias_has_two_ids():
    """DUPALIAS is listed as an alias of both GENEA and GENEB in the fixture."""
    tables = load_hgnc(COMPLETE_SET, WITHDRAWN)

    assert tables.alias["DUPALIAS"] == ["HGNC:1008", "HGNC:1009"]


def test_load_hgnc_withdrawn_set():
    tables = load_hgnc(COMPLETE_SET, WITHDRAWN)

    assert tables.withdrawn == {"OLDGENE1", "OLDGENE2"}
