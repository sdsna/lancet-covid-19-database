import ntpath
from helpers.load_indicator import load_indicator

# Load the dataframe for the given indicator based on the test name
def load_indicator_to_test(test_file_path):
    test_file = ntpath.basename(test_file_path)
    test_name = test_file.replace('_test.py', '')
    return load_indicator(test_name)
