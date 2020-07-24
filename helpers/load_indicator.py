import os
import pandas
from config import INDICATOR_FOLDER

# Load the dataframe for the given indicator
def load_indicator(name):
    file_name = os.path.join(INDICATOR_FOLDER, name + ".csv")
    return pandas.read_csv(file_name)
