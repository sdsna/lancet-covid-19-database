import pandas as pd
import datetime

from helpers.is_date import is_date
from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

# Let the user know that download is in progress
print("Downloading Google Mobility data (~100MB) — this may take a minute or two...")

dataset_url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv"

# Parse into dataframe
dataset = pd.read_csv(dataset_url, low_memory=False)

# Drop any rows with subnational observations
dataset = dataset[
    dataset[
        [
            "sub_region_1",
            "sub_region_2",
            "metro_area",
            "iso_3166_2_code",
            "census_fips_code",
        ]
    ]
    .isnull()
    .all(axis="columns")
]

# Normalize countries
dataset["iso_code"] = dataset["country_region"].apply(
    lambda country: normalize_country(country)
)

# Normalize date format
dataset["date"] = dataset["date"].apply(lambda date: normalize_date(date, "%Y-%m-%d"))


def run_pipeline(indicator):
    # Get the column name for this indicator
    column = (
        indicator.replace("google_mobility_change_", "", 1)
        + "_percent_change_from_baseline"
    )

    # Create slice of data with country ID, date, and indicator
    frame = dataset[["iso_code", "date", column]]

    # Rename column to indicator
    frame = frame.rename(columns={column: indicator})

    # Drop rows without observation
    frame = frame.dropna(subset=[indicator], axis="index")

    # Save as CSV file
    save_indicator(indicator, dataset=frame)
