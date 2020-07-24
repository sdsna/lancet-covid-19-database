import os
from config import INDICATOR_FOLDER

# Save the dataframe under the given name
def save_indicator(name, dataset):
    # Add column with indicator name
    dataset['indicator'] = name

    # Re-order columns
    dataset = dataset[['country', 'indicator', 'date', 'value']]

    # Sort by country ID, then date
    dataset = dataset.sort_values(by=['country', 'date'])

    # Save
    file_name = os.path.join(INDICATOR_FOLDER, name + ".csv")
    dataset.to_csv(file_name, index = False)
