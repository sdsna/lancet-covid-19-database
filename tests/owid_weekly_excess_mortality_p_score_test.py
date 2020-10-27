from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)


def test_united_kingdom():
    assert_value(103, "GBR", "2020-04-19", dataset)
