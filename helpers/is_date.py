import datetime

# Check if the provided string is a date of the given format
def is_date(string, format):
    try:
        datetime.datetime.strptime(string, format)
        return True
    except ValueError:
        return False
