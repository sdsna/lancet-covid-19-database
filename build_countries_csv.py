import os
import pandas
from config import COUNTRIES_PATH

codelist = pandas.read_csv('codelist.csv')

# Rename columns
codelist = codelist.rename(columns={'iso3c': 'id', 'country.name.en': 'name'})

# Keep only rows with ISO code
codelist = codelist.dropna(subset=['id'])

# Keep only ISO code and country name
codelist = codelist[['id', 'name']]

# Save
codelist.to_csv(COUNTRIES_PATH, index = False)
