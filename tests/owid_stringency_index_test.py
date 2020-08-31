from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)

def test_switzerland():
    assert_value(41.2, 'CHE', '2020-07-03', dataset)
