from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)


def test_belgium():
    assert_value(-60, "BEL", "2020-05-08", dataset)


def test_belgium():
    assert_value(-91, "NZL", "2020-03-29", dataset)
