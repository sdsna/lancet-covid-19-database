import os
import pandas
import numpy as np

from config import INDICATOR_FOLDER
from helpers.save_indicator import save_indicator

# Map our smoothed indicator ID to the source indicator
INDICATOR_MAP = {
    "new_cases_per_million": "owid_new_cases_per_million",
    "new_deaths_per_million": "owid_new_deaths_per_million",
    "effective_reproduction_rate": "marioli_effective_reproduction_rate",
    "positive_rate": "owid_positive_rate",
    "tests_per_case": "owid_tests_per_case",
}


def run_pipeline(indicator):
    # Get the source indicator
    key = indicator.replace("sdsn_", "").replace("_smoothed", "")
    source_indicator = INDICATOR_MAP[key]

    # Load the source dataset
    path_to_source_data = os.path.join(INDICATOR_FOLDER, source_indicator + ".csv")
    dataset = pandas.read_csv(path_to_source_data)

    # Drop country name
    dataset = dataset[["iso_code", "date", source_indicator]]

    # Convert date into index
    dataset["date"] = pandas.to_datetime(dataset["date"])
    dataset.set_index("date", inplace=True)

    # Generate rolling average over two week window, with at least 50% data
    # coverage. We use np.mean to average numbers, because it avoids weird
    # floating point issues when values are equal to zero:
    # See: https://groups.google.com/g/pydata/c/Bl7QLr-Y5Z0
    dataset[indicator] = (
        dataset.groupby("iso_code")[source_indicator]
        .rolling("14D", min_periods=7)
        .apply(np.mean)
        .reset_index(0, drop=True)
    )

    # Reshape date into column
    dataset["date"] = dataset.index
    dataset.reset_index(inplace=True, drop=True)

    # Drop rows without observations
    dataset = dataset.dropna(subset=[indicator], axis="index")

    # Save smoothed indicator
    save_indicator(indicator, dataset=dataset)
