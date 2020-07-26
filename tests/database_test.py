import pandas

from config import CODEBOOK_PATH, DATABASE_PATH, INDICATORS

database = pandas.read_csv(DATABASE_PATH)

def test_that_database_contains_all_indicators_defined_in_codebook():
    indicator_ids_used = database.indicator.unique()
    codebook = pandas.read_csv(CODEBOOK_PATH)
    indicators_defined_in_codebook = codebook['indicator'].tolist()
    assert indicator_ids_used.sort() == indicators_defined_in_codebook.sort()

def test_that_database_contains_all_indicators_defined_in_config():
    indicator_ids_used = database.indicator.unique()
    codebook = pandas.read_csv(CODEBOOK_PATH)
    indicators_defined_in_config = [x['id'] for x in INDICATORS]
    assert indicator_ids_used.sort() == indicators_defined_in_config.sort()
