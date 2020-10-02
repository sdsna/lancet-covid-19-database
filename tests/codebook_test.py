import pandas
import codecs
import re
from os import listdir
from os.path import isfile, join, splitext

from config import CODEBOOK_PATH, DATABASE_PATH, INDICATOR_FOLDER

codebook = pandas.read_csv(CODEBOOK_PATH)
indicators_defined_in_codebook = codebook["indicator"].tolist()


def test_that_codebook_is_utf8():
    try:
        codecs.open(CODEBOOK_PATH, encoding="utf-8", errors="strict").readlines()
        is_valid_utf8 = True
    except UnicodeDecodeError:
        is_valid_utf8 = False

    assert is_valid_utf8


def test_that_codebook_contains_exactly_one_entry_for_each_indicator():
    indicator_files = [
        splitext(f)[0]
        for f in listdir(INDICATOR_FOLDER)
        if isfile(join(INDICATOR_FOLDER, f))
    ]
    assert indicators_defined_in_codebook.sort() == indicator_files.sort()


def test_that_codebook_contains_all_indicators_used_in_database():
    database = pandas.read_csv(DATABASE_PATH, low_memory=False)
    indicator_ids_used = list(
        set(database.columns) - set(["iso_code", "country", "date"])
    )
    undefined_ids = list(set(indicator_ids_used) - set(indicators_defined_in_codebook))
    assert len(undefined_ids) == 0
