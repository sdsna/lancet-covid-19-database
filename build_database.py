import pandas as pd

from config import INDICATORS, DATABASE_PATH
from helpers.load_indicator import load_indicator

def build_database():
    # Collect indicator IDs
    indicator_ids = [x['id'] for x in INDICATORS]

    # Concatenate indicator files
    database = pd.concat([load_indicator(id) for id in indicator_ids ])

    # Save database
    database.to_csv(DATABASE_PATH, index = False)

if __name__ == '__main__':
    build_database()
