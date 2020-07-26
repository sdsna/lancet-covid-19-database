from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)

def test_germany_in_may():
    assert_value(175752, 'DEU', '2020-05-16', dataset)

def test_uk_aggregation():
    assert_value(298731, 'GBR', '2020-07-23', dataset)

def test_republic_of_congo():
    assert_value(0, 'COG', '2020-03-11', dataset)

def test_democratic_republic_of_congo():
    assert_value(1, 'COD', '2020-03-11', dataset)
