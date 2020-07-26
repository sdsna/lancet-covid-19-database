import os

# Configuration and settings

# The location of the data and indicator folder
DATA_FOLDER = 'data'
INDICATOR_FOLDER = os.path.join(DATA_FOLDER, 'indicators')
CODEBOOK_PATH = os.path.join(DATA_FOLDER, 'codebook.csv')
COUNTRIES_PATH = os.path.join(DATA_FOLDER, 'countries.csv')
DATABASE_PATH = os.path.join(DATA_FOLDER, 'database.csv')

# The format for the date column in the indicator CSV files
DATE_FORMAT = '%Y-%m-%d'

# The indicators and pipelines
INDICATORS = [
    {
        'id': 'jhu_cases',
        'pipeline': 'jhu',
        'dataset': 'time_series_covid19_confirmed_global.csv'
    },
    {
        'id': 'jhu_deaths',
        'pipeline': 'jhu',
        'dataset': 'time_series_covid19_deaths_global.csv'
    },
    {
        'id': 'jhu_recoveries',
        'pipeline': 'jhu',
        'dataset': 'time_series_covid19_recovered_global.csv'
    },
    {
        'id': 'owid_total_cases',
        'pipeline': 'owid',
        'column': 'total_cases'
    },
    {
        'id': 'owid_new_cases',
        'pipeline': 'owid',
        'column': 'new_cases'
    },
    {
        'id': 'owid_total_deaths',
        'pipeline': 'owid',
        'column': 'total_deaths'
    },
    {
        'id': 'owid_new_deaths',
        'pipeline': 'owid',
        'column': 'new_deaths'
    },
    {
        'id': 'owid_total_cases_per_million',
        'pipeline': 'owid',
        'column': 'total_cases_per_million'
    },
    {
        'id': 'owid_new_cases_per_million',
        'pipeline': 'owid',
        'column': 'new_cases_per_million'
    },
    {
        'id': 'owid_total_deaths_per_million',
        'pipeline': 'owid',
        'column': 'total_deaths_per_million'
    },
    {
        'id': 'owid_new_deaths_per_million',
        'pipeline': 'owid',
        'column': 'new_deaths_per_million'
    },
    {
        'id': 'owid_total_tests',
        'pipeline': 'owid',
        'column': 'total_tests'
    },
    {
        'id': 'owid_new_tests',
        'pipeline': 'owid',
        'column': 'new_tests'
    },
    {
        'id': 'owid_new_tests_smoothed',
        'pipeline': 'owid',
        'column': 'new_tests_smoothed'
    },
    {
        'id': 'owid_total_tests_per_thousand',
        'pipeline': 'owid',
        'column': 'total_tests_per_thousand'
    },
    {
        'id': 'owid_new_tests_per_thousand',
        'pipeline': 'owid',
        'column': 'new_tests_per_thousand'
    },
    {
        'id': 'owid_new_tests_smoothed_per_thousand',
        'pipeline': 'owid',
        'column': 'new_tests_smoothed_per_thousand'
    },
    {
        'id': 'owid_stringency_index',
        'pipeline': 'owid',
        'column': 'stringency_index'
    }
]
