import os
import pandas
from config import DATA_FOLDER

codelist = pandas.read_csv('codelist.csv')

# Rename columns
codelist = codelist.rename(columns={'iso3c': 'id', 'country.name.en': 'name'})

# Keep only rows with ISO code
codelist = codelist.dropna(subset=['id'])

# Keep only ISO code and country name
codelist = codelist[['id', 'name']]

# Save
file_name = os.path.join(DATA_FOLDER, 'countries.csv')
codelist.to_csv(file_name, index = False)
