import os
import pandas
from time import localtime, strftime

from config import INDICATOR_FOLDER
from helpers.save_indicator import save_indicator


# Carry forward the latest value from owid_positive_rate for up to seven days,
# to cover lags in data reporting


def run_pipeline(indicator):
    # Get smoothed positive rate
    positive_rate_path = os.path.join(INDICATOR_FOLDER, "owid_positive_rate.csv")
    dataset = pandas.read_csv(positive_rate_path)

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

    # Carry-forward the latest positive test rate for each country for up to
    # seven days
    dataset["carried_positive_rate_smoothed"] = (
        dataset.reset_index(level="iso_code")
        .groupby("iso_code")["owid_positive_rate"]
        .apply(lambda x: x.loc[x.last_valid_index() :].fillna(method="ffill", limit=7))
    )

    # Merge carried positive rate into the positive rate column
    dataset[indicator] = dataset["owid_positive_rate"].combine_first(
        dataset["carried_positive_rate_smoothed"]
    )

    # Reshape index back into columns
    dataset.reset_index(inplace=True)

    # Drop country name
    dataset = dataset[["iso_code", "date", indicator]]

    # Drop rows without classification
    dataset = dataset.dropna(subset=[indicator], axis="index")

    # Save as CSV file
    save_indicator(indicator, dataset=dataset)
