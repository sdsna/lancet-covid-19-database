import datetime
from config import DATE_FORMAT

# Normalize the date string into the format specified in config.py
def normalize_date(string, from_format):
    date = datetime.datetime.strptime(string, from_format)
    return date.strftime(DATE_FORMAT)
