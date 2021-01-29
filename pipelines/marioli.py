import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
import pandas

from helpers.normalize_date import normalize_date
from helpers.save_indicator import save_indicator
from helpers.normalize_country import normalize_country

# Request the website content from the Tracking R website
url = "http://trackingr-env.eba-9muars8y.us-east-2.elasticbeanstalk.com/_dash-update-component"
args = {
    "output": "page_content.children",
    "changedPropIds": ["url.pathname"],
    "inputs": [{"id": "url", "property": "pathname", "value": "/"}],
}
headers = {
    "Host": "trackingr-env.eba-9muars8y.us-east-2.elasticbeanstalk.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://trackingr-env.eba-9muars8y.us-east-2.elasticbeanstalk.com/",
    "Content-Type": "application/json",
    "X-CSRFToken": "undefined",
    "Origin": "http://trackingr-env.eba-9muars8y.us-east-2.elasticbeanstalk.com",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}
request = requests.post(url, json=args, headers=headers)
tracking_r_json = request.json()

# Extract the "Download Estimates (CSV)" link
json_search_needle = parse(
    '$..children[?`this` == "Download Estimates (CSV)"].`parent`.`parent`'
)
match = json_search_needle.find(tracking_r_json)[0]
url = match.value["href"]

# Download the CSV from Google Drive
download_url = "https://drive.google.com/uc?export=download&id=" + url.split("/")[-2]
dataset = pandas.read_csv(download_url)

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
