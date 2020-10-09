from helpers.load_indicator_to_test import load_indicator_to_test
from helpers.assert_value import assert_value
from helpers.assert_missing import assert_missing

# Load the indicator dataset
dataset = load_indicator_to_test(__file__)


def test_belarus():
    assert_value(0.264, "BLR", "2020-03-13", dataset, decimals=3)


# When less than 7 data points, no value should be reported
def test_belarus_less_than_7_datapoints():
    assert_missing("BLR", "2020-03-15", dataset)


# Even if a country has originally no data point for a given day,
# a value should be reported if data is available for 7 of the last
# 14 days.
def test_belarus_no_original_datapoint():
    assert_value(0.302, "BLR", "2020-03-14", dataset, decimals=3)
