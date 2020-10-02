import pandas as pd
import datetime

from helpers.is_date import is_date
from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.camel_case_to_snake_case import camel_case_to_snake_case

dataset_url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"

# Parse into dataframe
dataset = pd.read_csv(dataset_url, low_memory=False)

# Drop subnational data
dataset = dataset[dataset["RegionCode"].isnull()]

# Rename columns
dataset = dataset.rename(columns={"CountryCode": "iso_code", "Date": "date"})

# Normalize date format
dataset["date"] = dataset["date"].apply(
    lambda date: normalize_date(str(date), "%Y%m%d")
)


def normalize_column(column_name):
    normalized = column_name.replace(" ", "_").replace("/", "_or_")
    normalized = camel_case_to_snake_case(normalized)
    return "ox_" + normalized


def run_pipeline(indicator):
    # Get the column name for this indicator
    column = next(c for c in list(dataset.columns) if normalize_column(c) == indicator)

    # Create slice of data with country ID, date, and indicator
    frame = dataset[["iso_code", "date", column]]

    # Rename column to indicator
    frame = frame.rename(columns={column: indicator})

    # Drop rows without observation
    frame = frame.dropna(subset=[indicator], axis="index")

    # Save as CSV file
    save_indicator(indicator, dataset=frame)
