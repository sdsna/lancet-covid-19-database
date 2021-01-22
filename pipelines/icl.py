import pandas as pd
import datetime

from helpers.is_date import is_date
from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.camel_case_to_snake_case import camel_case_to_snake_case

dataset_url = (
    "https://raw.githubusercontent.com/RobertoFerC/SDSN_data_request/main/SDSN_Data.csv"
)

# Parse into dataframe
dataset = pd.read_csv(dataset_url, low_memory=False)

# Rename columns
dataset = dataset.rename(columns={"Country": "iso_code", "Date": "date"})

# Normalize date format
dataset["date"] = dataset["date"].apply(
    lambda date: normalize_date(str(date), "%Y-%m-%d")
)


def run_pipeline(indicator):
    # Rename value column to indicator
    frame = dataset.rename(columns={indicator.replace("icl_", ""): indicator})

    # Keep only relevant columns
    frame = frame[["iso_code", "date", indicator]]

    # Drop observations without indicator value
    frame = frame.dropna(subset=[indicator], axis="index")

    # Save as CSV file
    save_indicator(indicator, dataset=frame)
