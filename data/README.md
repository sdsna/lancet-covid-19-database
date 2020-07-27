# Lancet Data Extractions

![Last extraction](https://img.shields.io/endpoint?color=blue&label=Last%20extraction&url=https%3A%2F%2Fraw.githubusercontent.com%2Fsdsna%2Flancet-data%2Fmaster%2Fbadges%2Flast-extraction.json)
![Countries covered](https://img.shields.io/endpoint?color=blue&label=Countries%20covered&url=https%3A%2F%2Fraw.githubusercontent.com%2Fsdsna%2Flancet-data%2Fmaster%2Fbadges%2Fcountry-coverage.json)
![Days covered](https://img.shields.io/endpoint?color=blue&label=Days%20covered&url=https%3A%2F%2Fraw.githubusercontent.com%2Fsdsna%2Flancet-data%2Fmaster%2Fbadges%2Fday-coverage.json)
![Total indicators](https://img.shields.io/endpoint?color=blue&label=Total%20indicators&url=https%3A%2F%2Fraw.githubusercontent.com%2Fsdsna%2Flancet-data%2Fmaster%2Fbadges%2Ftotal-indicators.json)
![Total data points](https://img.shields.io/endpoint?color=blue&label=Total%20data%20points&url=https%3A%2F%2Fraw.githubusercontent.com%2Fsdsna%2Flancet-data%2Fmaster%2Fbadges%2Ftotal-data-points.json)

## Data Files

### [database.csv](https://sdsna.github.io/lancet-data/data/database.csv)

This is the full database including all indicators. Each row in the database consists of a country and a date. The row contains all available observations for the country on that date.

To open the database in Stata, run:
```stata
import delimited using database.csv, varnames(1) encoding("utf-8")
```

### [codebook.csv](https://sdsna.github.io/lancet-data/data/codebook.csv)

This file lists the indicator IDs used in the database and indicator files.
You will find the indicator label, description, notes, source, reference, and dataset links.

### [Indicator CSV Files](https://github.com/sdsna/lancet-data/tree/master/data/indicators/)

The `database.csv` file mentioned above contains all indicators. You can also
download data for specific indicators only. In the `indicators/` folder, you will find one CSV file for each indicator.

## Notes

1. Only countries (with 3166 ISO-3 code) have been retained. Observations for Kosovo and the Diamond Princess cruise ship, for example, have been removed.
1. Units for tests conducted vary between countries: tests performed vs people tested vs samples tested.

## Changelog

All additions, modifications, and deletions of indicators are tracked and logged
in [CHANGELOG.md](https://github.com/sdsna/lancet-data/blob/master/data/CHANGELOG.md).

## Questions? Comments? Concerns?

We would love to hear from you! If you have a GitHub account, feel free to [just post an issue](https://github.com/sdsna/lancet-data/issues).

Alternatively, you can contact Guillaume Lafortune at guillaume.lafortune@unsdsn.org
or Finn Woelm at finn.woelm@unsdsn.org.
