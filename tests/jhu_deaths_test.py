from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)

def test_united_states():
    assert_value(140756, 'USA', '2020-07-18', dataset)

def test_netherlands_aggregation():
    assert_value(6076, 'NLD', '2020-06-13', dataset)
