import codecs
from config import CODEBOOK_PATH

def test_that_codebook_is_utf8():
    try:
        codecs.open(CODEBOOK_PATH, encoding="utf-8", errors="strict").readlines()
        is_valid_utf8 = True
    except UnicodeDecodeError:
        is_valid_utf8 = False

    assert is_valid_utf8
