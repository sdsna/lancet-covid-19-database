import os
import pandas
import numpy as np
from time import localtime, strftime

from config import INDICATOR_FOLDER
from helpers.save_indicator import save_indicator

# Map our smoothed indicator ID to the source indicator
INDICATOR_MAP = {
    "new_cases_per_million": "owid_new_cases_per_million",
    "new_deaths_per_million": "owid_new_deaths_per_million",
    "effective_reproduction_rate": "marioli_effective_reproduction_rate",
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

    # Index on iso_code and date
    dataset["date"] = pandas.to_datetime(dataset["date"])
    dataset = dataset.set_index(["iso_code", "date"])

    # Identify first and last date
    today = strftime("%Y-%m-%d", localtime())
    dates = dataset.index.get_level_values("date")
    dates = dates.append(pandas.DatetimeIndex([pandas.to_datetime(today)]))

    # Fill missing days in dataset
    timerange = pandas.date_range(dates.min(), dates.max(), freq="D")
    dataset = dataset.reindex(
        pandas.MultiIndex.from_product(
            [dataset.index.levels[0], timerange], names=["iso_code", "date"]
        ),
    )

    # Generate rolling average over two week window, with at least 50% data
    # coverage. We use np.mean to average numbers, because it avoids weird
    # floating point issues when values are equal to zero:
    # See: https://groups.google.com/g/pydata/c/Bl7QLr-Y5Z0
    dataset[indicator] = (
        dataset.reset_index(level="iso_code")
        .groupby("iso_code")[source_indicator]
        .rolling("14D", min_periods=7)
        .apply(np.mean)
    )

    # Reshape index back into columns
    dataset.reset_index(inplace=True)

    # Drop rows without observations
    dataset = dataset.dropna(subset=[indicator], axis="index")

    # Save smoothed indicator
    save_indicator(indicator, dataset=dataset)
