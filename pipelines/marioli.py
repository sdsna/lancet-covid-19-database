import requests
from urllib.parse import unquote
import pandas
import io

from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

# This request replicates the request made by the browser when clicking on
# "Download Estimates (CSV)" on the website.
url = "http://trackingr-env.eba-9muars8y.us-east-2.elasticbeanstalk.com/_dash-update-component"
args = {
    "output": "..download_link.href...download_link.download..",
    "changedPropIds": ["download_link.n_clicks"],
    "inputs": [{"id": "download_link", "property": "n_clicks", "value": 1}],
}
request = requests.post(url, json=args)

# Extract the CSV string from the JSON response
json = request.json()
csv = json["response"]["download_link"]["href"]

# Remove the "data:text/csv;charset=utf-8" part from the string
csv = csv[csv.find(",") + 1 :]

# URL-decode the CSV string
csv = unquote(csv)

# Read CSV string with pandas
csv_buffer = io.StringIO(csv)
dataset = pandas.read_csv(csv_buffer)

# Keep rows with average serial interval of 7 only
dataset = dataset[dataset["days_infectious"] == 7]

# Rename columns
dataset = dataset.rename(
    columns={"Country/Region": "country", "R": "effective_reproduction_rate"}
)

# Convert countries to iso_code:
# * Remove non-ISO countries
dataset = dataset[~dataset["country"].isin(["World", "Kosovo"])]
# * Perform conversion
dataset["iso_code"] = dataset["country"].apply(
    lambda country: normalize_country(country)
)

# Normalize date format
dataset["date"] = dataset["Date"].apply(lambda date: normalize_date(date, "%Y-%m-%d"))


def run_pipeline(indicator):
    # Set column name from indicator
    column = indicator.replace("marioli_", "")

    # Create slice of data with country ID, date, and indicator
    frame = dataset[["iso_code", "date", column]]

    # Rename column to indicator
    frame = frame.rename(columns={column: indicator})

    # Drop rows without observation
    frame = frame.dropna(subset=[indicator], axis="index")

    save_indicator(indicator, dataset=frame)
