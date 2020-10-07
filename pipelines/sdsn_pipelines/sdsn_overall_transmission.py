import os
import pandas

from config import INDICATOR_FOLDER
from helpers.save_indicator import save_indicator


def generate_classification(row):
    tests_per_case = row["tests_per_case_smoothed"]
    daily_cases_per_million = row["daily_cases_per_million_smoothed"]

    # If tests per case are missing, set no classification
    if pandas.isna(tests_per_case) or pandas.isna(daily_cases_per_million):
        return None

    # Suppression
    if (daily_cases_per_million <= 5) and (tests_per_case >= 20):
        return 1

    # Low
    if daily_cases_per_million <= 10:
        return 2

    # Moderate
    if daily_cases_per_million <= 50:
        return 3

    # High
    if daily_cases_per_million <= 100:
        return 4

    # Very high
    if daily_cases_per_million > 100:
        return 5


def run_pipeline(indicator):
    # Get smoothed daily cases per million
    daily_cases_per_million_path = os.path.join(
        INDICATOR_FOLDER, "sdsn_daily_cases_per_million_smoothed.csv"
    )
    daily_cases_per_million = pandas.read_csv(daily_cases_per_million_path)
    daily_cases_per_million.rename(
        columns={
            "sdsn_daily_cases_per_million_smoothed": "daily_cases_per_million_smoothed"
        },
        inplace=True,
    )

    # Get smoothed tests per case
    tests_per_case_path = os.path.join(
        INDICATOR_FOLDER, "sdsn_tests_per_case_smoothed.csv"
    )
    tests_per_case = pandas.read_csv(tests_per_case_path)
    tests_per_case.rename(
        columns={"sdsn_tests_per_case_smoothed": "tests_per_case_smoothed"},
        inplace=True,
    )

    # Merge datasets
    dataset = pandas.merge(
        daily_cases_per_million,
        tests_per_case,
        how="outer",
        on=["iso_code", "country", "date"],
    )

    # Generate classification
    dataset[indicator] = dataset.apply(generate_classification, axis=1)

    # Drop country name
    dataset = dataset[["iso_code", "date", indicator]]

    # Drop rows without classification
    dataset = dataset.dropna(subset=[indicator], axis="index")

    # Save as CSV file
    save_indicator(indicator, dataset=dataset)
