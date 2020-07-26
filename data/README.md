# Lancet Data Extractions

## Data Files

### [database.csv](https://sdsna.github.io/lancet-data/data/database.csv)

This is the full database including all indicators. Each row in the database represents one observation. Each observation consists of a country ID, and indicator ID, a date, and a value.

To open the database in Stata, run:
```stata
import delimited using database.csv, varnames(1) encoding("utf-8")
```

Prefer a table over a list? You can transpose the data in Stata using reshape:

```stata
// Convert indicator IDs into valid variable names: Replace dashes with
// underscores and retain only the first 26 characters
replace indicator = substr(strtoname(indicator), 1, 26) + "_"

// Transpose into table format using reshape
reshape wide @value, i(country date) j(indicator) string
```

![A picture of the database transposed in Stata](https://raw.githubusercontent.com/sdsna/lancet-data/master/transposed-database.png)

### [codebook.csv](https://sdsna.github.io/lancet-data/data/codebook.csv)

This file lists the indicator IDs used in the database and indicator files.
You will find the indicator label, description, notes, source, reference, and dataset links.

### [countries.csv](https://sdsna.github.io/lancet-data/data/countries.csv)

This file lists the country IDs used in the database and indicator files.
The IDs used are the ISO 3166 3-letter codes.

### [Indicator CSV Files](https://github.com/sdsna/lancet-data/tree/master/data/indicators/)

The `database.csv` file mentioned above contains all indicators. You can also
download data for specific indicators only. In the `indicators/` folder, you will find one CSV file for each indicator.

## Notes

1. Only countries (with 3166 ISO-3 code) have been retained. Observations for Kosovo and the Diamond Princess cruise ship, for example, have been removed.
1. Units for tests conducted vary between countries: tests performed vs people tested vs samples tested.

## Questions? Comments? Concerns?

We would love to hear from you! If you have a GitHub account, feel free to [just post an issue](https://github.com/sdsna/lancet-data/issues).

Alternatively, you can contact Guillaume Lafortune at guillaume.lafortune@unsdsn.org
or Finn Woelm at finn.woelm@unsdsn.org.
