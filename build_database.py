import pandas as pd

from config import INDICATORS, DATABASE_PATH
from helpers.load_indicator import load_indicator

def build_database():
    # Collect indicator IDs
    indicator_ids = [x['id'] for x in INDICATORS]

    # Load first indicator
    database = load_indicator(indicator_ids[0])

    # Merge indicator files on ID and date
    for id in indicator_ids[1:]:
        dataset = load_indicator(id)
        database = pd.merge(database, dataset,
                            how = 'outer', on = ['country', 'date'])

    # Save database
    database.to_csv(DATABASE_PATH, index = False)

if __name__ == '__main__':
    build_database()
