import pandas as pd

from config import DATABASE_PATH
from helpers.load_indicator import load_indicator
from helpers.get_indicator_ids import get_indicator_ids

def build_database():
    # Collect indicator IDs
    indicator_ids = get_indicator_ids()

    # Load first indicator
    database = load_indicator(indicator_ids[0])

    # Merge indicator files on ID and date
    for id in indicator_ids[1:]:
        dataset = load_indicator(id)
        database = pd.merge(database, dataset,
                            how = 'outer', on = ['iso_code', 'country', 'date'])

    # Save database
    database.to_csv(DATABASE_PATH, index = False)

if __name__ == '__main__':
    build_database()
