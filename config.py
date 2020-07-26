import os

# Configuration and settings

# The location of the data and indicator folder
DATA_FOLDER = 'data'
INDICATOR_FOLDER = os.path.join(DATA_FOLDER, 'indicators')
CODEBOOK_PATH = os.path.join(DATA_FOLDER, 'codebook.csv')

# The format for the date column in the indicator CSV files
DATE_FORMAT = '%Y-%m-%d'

# The indicators and pipelines
INDICATORS = [
    {
        'id': 'jhu-cases',
        'pipeline': 'jhu',
        'dataset': 'time_series_covid19_confirmed_global.csv'
    },
    {
        'id': 'jhu-deaths',
        'pipeline': 'jhu',
        'dataset': 'time_series_covid19_deaths_global.csv'
    },
    {
        'id': 'jhu-recoveries',
        'pipeline': 'jhu',
        'dataset': 'time_series_covid19_recovered_global.csv'
    },
]
