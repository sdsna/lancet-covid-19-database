import pandas as pd
import datetime

from helpers.is_date import is_date
from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

file_map = {
    "jhu_confirmed": "time_series_covid19_confirmed_global.csv",
    "jhu_deaths": "time_series_covid19_deaths_global.csv",
    "jhu_recovered": "time_series_covid19_recovered_global.csv",
}

repository_url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/"


def run_pipeline(indicator):
    # Parse into dataframe
    url = repository_url + file_map[indicator]
    data = pd.read_csv(url)

    # Relabel country and state column
    data = data.rename(columns={"Country/Region": "country", "Province/State": "state"})

    # Keep country, state, and dates only
    data = data[
        ["country", "state"]
        + [column for column in data if is_date(column, "%m/%d/%y")]
    ]

    # Normalize country names:
    # * Drop non-countries
    data = data[
        ~data.country.isin(
            ["Diamond Princess", "MS Zaandam", "Kosovo", "Summer Olympics 2020"]
        )
    ]
    # * Fix Taiwan: It is not clear why there is a star next to the name
    data["country"] = data["country"].replace({"Taiwan*": "Taiwan"})
    # * Fix Micronesia: Micronesia refers to the Federated States
    data["country"] = data["country"].replace(
        {"Micronesia": "Micronesia, Federated States of"}
    )
    # * Perform conversion
    data["iso_code"] = data["country"].apply(lambda country: normalize_country(country))
    # * Drop country name
    data = data.drop(columns=["country"])

    # Reshape into list
    data = data.melt(id_vars=["iso_code", "state"])
    data = data.rename(columns={"variable": "date", "value": indicator})

    # Normalize date format
    data["date"] = data["date"].apply(lambda date: normalize_date(date, "%m/%d/%y"))

    # Verify uniqueness
    if data.duplicated(["iso_code", "state", "date"]).any(axis=None):
        raise Exception("Duplicates in data detected")

    # Collapse states into country
    data = data.groupby(["iso_code", "date"], as_index=False).agg("sum")

    # Save as CSV file
    save_indicator(indicator, dataset=data)
