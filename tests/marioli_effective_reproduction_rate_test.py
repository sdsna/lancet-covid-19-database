from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)


def test_india():
    assert_value(1.22, "IND", "2020-06-30", dataset, decimals=2)


def test_united_states():
    assert_value(1.21, "USA", "2020-07-10", dataset, decimals=2)
