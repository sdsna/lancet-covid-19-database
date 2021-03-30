from urllib.request import Request, urlopen
import pandas as pd
import datetime

from helpers.is_date import is_date
from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

dataset_url = (
    "https://covid.ourworldindata.org/data/excess_mortality/excess_mortality.csv"
)

req = Request(dataset_url)
req.add_header(
    "User-Agent",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
)
content = urlopen(req)

# Parse into dataframe
dataset = pd.read_csv(content)

# Normalize date format
dataset["date"] = dataset["date"].apply(lambda date: normalize_date(date, "%Y-%m-%d"))

# Rename p-score columns
new_column_names = {}
for column in dataset.columns:
    new_column_names[column] = (
        column.replace("p_scores_", "weekly_excess_mortality_p_score_")
        .replace("_all_ages", "")
        .replace("average_", "avg_")
        .replace("deaths_", "weekly_deaths_")
    )

dataset.rename(columns=new_column_names, inplace=True)

# Normalize country names:
# * Drop non countries
dataset = dataset[
    ~dataset.location.isin(
        ["England & Wales", "Northern Ireland", "Scotland", "Transnistria"]
    )
]
# * Perform conversion
dataset["iso_code"] = dataset["location"].apply(
    lambda country: normalize_country(country)
)


def run_pipeline(indicator):
    # Get the column name for this indicator
    column = indicator.replace("owid_", "", 1)

    # Create slice of data with country ISO, date, and indicator
    frame = dataset[["iso_code", "date", column]]

    # Rename column to indicator
    frame = frame.rename(columns={column: indicator})

    # Drop rows without observation
    frame = frame.dropna(subset=[indicator], axis="index")

    # Save as CSV file
    save_indicator(indicator, dataset=frame)
