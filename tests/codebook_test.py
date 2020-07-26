import pandas
import codecs
from os import listdir
from os.path import isfile, join, splitext

from config import CODEBOOK_PATH, INDICATOR_FOLDER

def test_that_codebook_is_utf8():
    try:
        codecs.open(CODEBOOK_PATH, encoding="utf-8", errors="strict").readlines()
        is_valid_utf8 = True
    except UnicodeDecodeError:
        is_valid_utf8 = False

    assert is_valid_utf8

def test_that_codebook_contains_exactly_one_entry_for_each_indicator():
    indicator_files = [splitext(f)[0] for f in listdir(INDICATOR_FOLDER) if isfile(join(INDICATOR_FOLDER, f))]
    codebook = pandas.read_csv(CODEBOOK_PATH)
    indicators = codebook['indicator'].tolist()

    assert indicators.sort() == indicator_files.sort()
