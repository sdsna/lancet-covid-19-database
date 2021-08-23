import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
import pandas

from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

# Download the CSV from Google Drive
download_url = "https://raw.githubusercontent.com/crondonm/TrackingR/main/Estimates-Database/database.csv"
dataset = pandas.read_csv(download_url)

# Keep rows with average serial interval of 7 only
dataset = dataset[dataset["days_infectious"] == 7]

# Rename columns
dataset = dataset.rename(
    columns={"Country/Region": "country", "R": "effective_reproduction_rate"}
)

# Convert countries to iso_code:
# * Remove non-ISO countries
dataset = dataset[~dataset["country"].isin(["World", "Kosovo", "Summer Olympics 2020"])]
# * Perform conversion
dataset["iso_code"] = dataset["country"].apply(
    lambda country: normalize_country(country)
)

# Normalize date format
dataset["date"] = dataset["Date"].apply(lambda date: normalize_date(date, "%Y-%m-%d"))


def run_pipeline(indicator):
    # Set column name from indicator
    column = indicator.replace("marioli_", "")

    # Create slice of data with country ID, date, and indicator
    frame = dataset[["iso_code", "date", column]]

    # Rename column to indicator
    frame = frame.rename(columns={column: indicator})

    # Drop rows without observation
    frame = frame.dropna(subset=[indicator], axis="index")

    save_indicator(indicator, dataset=frame)
