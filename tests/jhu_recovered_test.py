from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)

def test_india():
    assert_value(91852, 'IND', '2020-05-31', dataset)

def test_china_aggregation():
    assert_value(79434, 'CHN', '2020-06-07', dataset)
