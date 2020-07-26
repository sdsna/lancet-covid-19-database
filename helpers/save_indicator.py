import os
from config import INDICATOR_FOLDER

# Save the dataframe under the given name
def save_indicator(name, dataset):
    # Verify there are no empty countries or dates
    nulls = dataset[['country', 'date']].isnull()
    if nulls.any(axis=None):
        raise Exception('Null values for country/date detected')

    # Verify that there are no duplicate entries for country and date
    if dataset.duplicated(['country', 'date']).any(axis=None):
        raise Exception('Duplicate country-data in data detected')

    # Re-order columns
    dataset = dataset[['country', 'date', name]]

    # Sort by country ID, then date
    dataset = dataset.sort_values(by=['country', 'date'])

    # Save
    file_name = os.path.join(INDICATOR_FOLDER, name + ".csv")
    dataset.to_csv(file_name, index = False)
