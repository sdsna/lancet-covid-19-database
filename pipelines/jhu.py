import pandas as pd
import datetime

from helpers.is_date import is_date
from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

repository_url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/"

def run_pipeline(indicator, dataset):
    # Parse into dataframe
    url = repository_url + dataset
    data = pd.read_csv(url)

    # Relabel country and state column
    data = data.rename(columns={'Country/Region': 'country', 'Province/State': 'state'})

    # Keep country, state, and dates only
    data = data[['country', 'state'] + [column for column in data if is_date(column, '%m/%d/%y')]]

    # Normalize country names:
    # * Drop non-countries
    data = data.drop(data[data.country.isin(["Diamond Princess", "MS Zaandam"])].index)
    # * Fix Taiwan: It is not clear why there is a star next to the name
    data['country'] = data['country'].replace({'Taiwan*': 'Taiwan'})
    # * Perform conversion
    data['country'] = data['country'].apply(lambda country: normalize_country(country))

    # Reshape into list
    data = data.melt(id_vars=['country', 'state'])
    data = data.rename(columns={'variable': 'date'})

    # Normalize date format
    data['date'] = data['date'].apply(lambda date: normalize_date(date, '%m/%d/%y'))

    # Verify uniqueness
    if data.duplicated(['country', 'state', 'date']).any(axis=None):
        raise Exception('Duplicates in data detected')

    # Collapse states into country
    data = data.groupby(["country", "date"], as_index=False).agg('sum')

    # Save as CSV file
    save_indicator(indicator, dataset=data)
