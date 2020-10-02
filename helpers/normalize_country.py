import pandas
import re

codelist = pandas.read_csv("helpers/codelist.csv")

# Remove rows without iso3 code
codelist = codelist.dropna(subset=["iso3c"], axis="index")

# Normalize the country string into ISO 3166 alpha-3 country code
# See: https://en.wikipedia.org/wiki/ISO_3166
# Note:
# The codelist file with country regexes comes from the countrycode R package
# Available for download here: https://github.com/vincentarelbundock/countrycode/blob/master/dictionary/codelist_without_cldr.csv
def normalize_country(country):
    matches = codelist[
        codelist["country.name.en.regex"].apply(
            lambda x: True if re.search(x, country, re.IGNORECASE) else False
        )
    ]

    if len(matches) == 1:
        return matches["iso3c"].values[0]
    else:
        raise Exception("Could not find exactly one ISO-3 code for " + country, matches)
