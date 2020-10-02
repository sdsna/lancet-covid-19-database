import pandas

from config import CODEBOOK_PATH, DATABASE_PATH

database = pandas.read_csv(DATABASE_PATH, low_memory=False)
indicator_ids_in_db = list(set(database.columns) - set(["iso_code", "country", "date"]))


def test_that_database_contains_all_indicators_defined_in_codebook():
    codebook = pandas.read_csv(CODEBOOK_PATH)
    indicators_defined_in_codebook = codebook["indicator"].tolist()
    assert indicator_ids_in_db.sort() == indicators_defined_in_codebook.sort()


def test_that_there_are_no_empty_rows():
    df = database.loc[:, ~database.columns.isin(["iso_code", "country", "date"])]
    df = df.isnull().all(axis="columns")
    rows_that_are_empty = list(df.index[df])
    assert len(rows_that_are_empty) == 0


def test_that_there_are_no_duplicates():
    duplicates = database.duplicated(["iso_code", "date"])
    rows_that_are_duplicates = list(duplicates.index[duplicates])
    assert len(rows_that_are_duplicates) == 0
