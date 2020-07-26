# Lancet Data Extractions

## Data

All data can be found in the `/data/` folder.

### database.csv

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

![A picture of the database transposed in Stata](/transposed-database.png?raw=true)

### codebook.csv

This file lists the indicator IDs used in the database and indicator files.
You will find the indicator label, description, notes, source, reference, and dataset links.

### countries.csv

This file lists the country IDs used in the database and indicator files.
The IDs used are the ISO 3166 3-letter codes.

### indicators/[xyz].csv

The database.csv file mentioned above contains all indicators. You can also
download data for specific indicators only. In the `/data/indicators/` folder, you will find one CSV file for each indicator.

## Notes

1. Only countries are retained. Diamond Princess, for example, is not.

## Questions? Comments? Concerns?

If you have a GitHub account, please post an issue.

You can also contact Guillaume Lafortune at guillaume.lafortune@unsdsn.org
or Finn Woelm at finn.woelm@unsdsn.org.

---

## Development Notes

The extraction code is written in Python.

### Testing

To test the extractions, run `pytest`. It invokes tests defined in the
`/tests` folder.
