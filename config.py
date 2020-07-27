import os

# Configuration and settings

# The location of the data and indicator folder
DATA_FOLDER = 'data'
BADGES_FOLDER = 'badges'
INDICATOR_FOLDER = os.path.join(DATA_FOLDER, 'indicators')
CODEBOOK_PATH = os.path.join(DATA_FOLDER, 'codebook.csv')
COUNTRIES_PATH = os.path.join(DATA_FOLDER, 'countries.csv')
DATABASE_PATH = os.path.join(DATA_FOLDER, 'database.csv')

# The format for the date column in the indicator CSV files
DATE_FORMAT = '%Y-%m-%d'
