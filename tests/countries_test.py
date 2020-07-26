import pandas
import codecs
from os import listdir
from os.path import isfile, join, splitext

from config import COUNTRIES_PATH, DATABASE_PATH

def test_that_file_is_utf8():
    try:
        codecs.open(COUNTRIES_PATH, encoding="utf-8", errors="strict").readlines()
        is_valid_utf8 = True
    except UnicodeDecodeError:
        is_valid_utf8 = False

    assert is_valid_utf8

def test_that_file_contains_all_ids_used_in_database():
    countries = pandas.read_csv(COUNTRIES_PATH)
    ids_defined_in_file = countries['id'].tolist()
    database = pandas.read_csv(DATABASE_PATH)
    country_ids_used = database.country.unique()
    undefined_ids = list(set(country_ids_used) - set(ids_defined_in_file))
    assert len(undefined_ids) == 0
