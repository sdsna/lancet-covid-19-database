from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)

def test_germany():
    assert_value(23, 'DEU', '2020-03-04', dataset)

def test_singapore():
    assert_value(57, 'SGP', '2020-07-07', dataset)
