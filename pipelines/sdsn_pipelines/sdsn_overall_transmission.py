import os
import pandas

from config import INDICATOR_FOLDER
from helpers.save_indicator import save_indicator


def generate_classification(row):
    tests_per_case = row["tests_per_case_smoothed"]
    new_cases_per_million = row["new_cases_per_million_smoothed"]

    # We make an exception for China, as requested by Jeffrey Sachs:
    # And for China, we know the incidence is so low and the testing so
    # extensive whenever there is an outbreak (comprehensive testing, for
    # example, in Beijing and Wuhan after small outbreaks) that China should be
    # classified as having sufficient testing, so just based on new cases.
    if row["iso_code"] == "CHN":
        tests_per_case = 100

    # Whether the country has testing data
    has_test_data = not pandas.isna(tests_per_case)

    # If new_cases_per_million are missing, set no classification
    if pandas.isna(new_cases_per_million):
        return None

    # Suppression
    if (new_cases_per_million <= 5) and (tests_per_case >= 20):
        return 1

    # Low
    if new_cases_per_million <= 10 and has_test_data:
        return 2

    # Moderate
    if new_cases_per_million <= 50 and has_test_data:
        return 3

    # High
    if new_cases_per_million <= 100 and has_test_data:
        return 4

    # Very high if a lot of new cases per million, even if no test data
    if new_cases_per_million > 100:
        return 5


def run_pipeline(indicator):
    # Get smoothed daily cases per million
    daily_cases_per_million_path = os.path.join(
        INDICATOR_FOLDER, "sdsn_new_cases_per_million_smoothed.csv"
    )
    daily_cases_per_million = pandas.read_csv(daily_cases_per_million_path)
    daily_cases_per_million.rename(
        columns={
            "sdsn_new_cases_per_million_smoothed": "new_cases_per_million_smoothed"
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
