# Create JSON for shields.io badges
# See: https://shields.io/endpoint

import os
import json
from time import gmtime, strftime
import pandas
from millify import millify

from config import BADGES_FOLDER, DATABASE_PATH, CODEBOOK_PATH

BADGE_TEMPLATE = {"schemaVersion": 1, "label": None, "message": None}

# Set full_extraction = True, if the full dataset has been extracted.
# This will regenerate the last-extraction badge with a timestamp of now
def make_badges(full_extraction=False):
    badges = {}

    # Load the database and codebook
    database = pandas.read_csv(DATABASE_PATH, low_memory=False)
    codebook = pandas.read_csv(CODEBOOK_PATH)

    # Last update badge
    if full_extraction:
        badges["last-extraction"] = strftime("%b %d, %Y %H:%M GMT", gmtime())

    # Countries covered
    badges["country-coverage"] = database["iso_code"].nunique()

    # Days covered
    badges["day-coverage"] = database["date"].nunique()

    # Total indicators
    badges["total-indicators"] = codebook["indicator"].count()

    # Total observations
    indicators = codebook["indicator"].tolist()
    values_frame = database[indicators]
    observations = values_frame.count(axis="columns").sum()
    badges["total-data-points"] = millify(observations, precision=1)

    # Write badges
    for key, value in badges.items():
        # Copy the template
        badge = BADGE_TEMPLATE.copy()

        # Update the message and label
        badge["label"] = key
        badge["message"] = str(value)

        # Save the updated badge content
        with open(os.path.join(BADGES_FOLDER, key + ".json"), "w") as file:
            json.dump(badge, file, indent=2)


if __name__ == "__main__":
    make_badges()
