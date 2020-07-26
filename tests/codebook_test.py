import pandas
import codecs
import re
from os import listdir
from os.path import isfile, join, splitext

from config import CODEBOOK_PATH, DATABASE_PATH, INDICATOR_FOLDER

codebook = pandas.read_csv(CODEBOOK_PATH)
indicators_defined_in_codebook = codebook['indicator'].tolist()

def test_that_codebook_is_utf8():
    try:
        codecs.open(CODEBOOK_PATH, encoding="utf-8", errors="strict").readlines()
        is_valid_utf8 = True
    except UnicodeDecodeError:
        is_valid_utf8 = False

    assert is_valid_utf8

def test_that_codebook_contains_exactly_one_entry_for_each_indicator():
    indicator_files = [splitext(f)[0] for f in listdir(INDICATOR_FOLDER) if isfile(join(INDICATOR_FOLDER, f))]
    assert indicators_defined_in_codebook.sort() == indicator_files.sort()

def test_that_codebook_contains_all_indicators_used_in_database():
    database = pandas.read_csv(DATABASE_PATH)
    indicator_ids_used = database.indicator.unique()
    undefined_ids = list(set(indicator_ids_used) - set(indicators_defined_in_codebook))
    assert len(undefined_ids) == 0

# Stata variables have a maximum length of 32. When transposing the dataset,
# the indicator ID must be trimmed to 26 characters. The remaining 6 characters
# are used by "_value". We need to make sure that the first 26 characters of
# every indicator ID are unique.
def test_that_indicator_ids_create_unique_stata_variables():
    trimmed_ids = []
    for id in indicators_defined_in_codebook:
        # Replace non-alphanumeric characters with underscore
        clean_id = re.sub("[^0-9a-zA-Z]+", "_", id)
        # Retain only the first 26 characters
        trimmed_ids.append(clean_id[:26])

    duplicate_ids = [x for x in trimmed_ids if trimmed_ids.count(x) > 1]
    assert len(duplicate_ids) == 0
