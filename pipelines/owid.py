import pandas as pd
import datetime

from helpers.is_date import is_date
from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

dataset_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

# Parse into dataframe
dataset = pd.read_csv(dataset_url, low_memory = False)

# Relabel country ID column
dataset = dataset.rename(columns={'iso_code': 'country'})

# Drop non-countries
dataset = dataset.drop(dataset[dataset.location == "International"].index)
dataset = dataset.drop(dataset[dataset.country.isin(['OWID_KOS', 'OWID_WRL'])].index)

# Normalize date format
dataset['date'] = dataset['date'].apply(lambda date: normalize_date(date, '%Y-%m-%d'))


def run_pipeline(indicator, column):
    # Create slice of data with country, date, and indicator
    frame = dataset[['country', 'date', column]]

    # Rename column to value
    frame = frame.rename(columns = { column: 'value' })

    # Save as CSV file
    save_indicator(indicator, dataset=frame)
