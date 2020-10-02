from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)


def test_luxembourg():
    assert_value(2, "LUX", "2020-06-18", dataset)
