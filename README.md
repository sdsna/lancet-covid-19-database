# ⚠ Archive Notice ⚠

The COVID-19 Data Portal of the Lancet COVID-19 Commission has been archived. It is now read-only. The data is no longer being updated and the indicator set is no longer being maintained. On our [indicators page](https://data.covid19commission.org/indicators), you will find references and links to the source data sets which will allow you to check for data updates directly with the data providers.

# Lancet Data Extractions

## Data

You can find the full database, codebook, and indicator files in [the `/data/` folder](https://github.com/sdsna/lancet-covid-19-database/tree/master/data).

---

## Development Notes

The extraction code is written in Python.

### Prerequisites

You will need `git`, `python`, and `pipenv`.

1. [Download and install `git`](https://git-scm.com/downloads)
1. Download and install `python`: [Windows](https://docs.python-guide.org/starting/install3/win/#install3-windows), [Mac OS X](https://docs.python-guide.org/starting/install3/osx/#install3-osx), [Linux](https://docs.python-guide.org/starting/install3/linux/#install3-linux)
1. Once you have `python`, you will need to install `pipenv`. In the terminal, run: `pip install pipenv`

Need help? Feel free to reach out to finn.woelm@unsdsn.org.

### Setup

Run the following commands in the terminal.

First, clone this GitHub repository to your computer:

```bash
cd ~/whatever/folder/you/want/to/use
git clone https://github.com/sdsna/lancet-covid-19-database.git
cd ./lancet-covid-19-database/
```

Then, set up the python environment:

```bash
pipenv install
```

Then, enter into the python shell:

```bash
pipenv shell
```

If everything worked, you can now run the test suite:

```bash
pytest
```

You should see a lot of green text, saying that tests have passed.

### Updating Datasets

Before updating your datasets, make sure your local copy of this repository is
up to date:

```bash
git pull
```

To update all datasets, run:

```bash
python extract_indicator.py "*"
```

To update a specific dataset, run:

```bash
python extract_indicator.py jhu_confirmed
```

You can use wildcards (`*` and `?`) to extract several indicators at once:

```bash
python extract_indicator.py "owid_*"
```

After updating the datasets, the script will take care of rebuilding the database.

At the very end, should see this in the terminal:

```bash
Rebuilding database ...
Rebuilding database ... Done! :)
Remaking badges ...
Remaking badges ... Done! :)
```

### Publishing to GitHub

To publish updated datasets to GitHub, create a new commit with the updated indicator files and the overall database.

```bash
git add ./data/ ./badges/
git commit -m "Update indicators (YYYY-MM-DD)"
git push
```

### Troubleshooting

Sometimes, things may go wrong. A close look at the error message you get may help you understand what is happening.

Here are three common errors and their fixes:

#### Error during `git push`

You may encounter an error during `git push`, if your local copy of the repository is out of sync with the copy on GitHub. This error looks something like this:

```bash
$ git push
To https://github.com/sdsna/lancet-covid-19-database.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/sdsna/lancet-covid-19-database.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

The solution is to reset your local repository to the state of the repository on GitHub. Warning: Any changes you have made to the code locally will be overwritten!

```shell
git fetch
git reset --hard origin/master
```

Now you can redo the steps for [updating the data](#updating-datasets) and [publishing to GitHub](#publishing-to-github). This time it will succeed.

#### `PermissionError` when updating the data

You may encounter a `PermissionError` while updating the datasets:

```shell
Rebuilding database ...
Traceback (most recent call last):
  File ".\extract_indicator.py", line 45, in <module>
    build_database()
  File "C:\Users\Finn Woelm\Projects\lancet-covid-19-database\build_database.py", line 21, in build_database
    database.to_csv(DATABASE_PATH, index = False)
  File "C:\Users\Finn Woelm\.virtualenvs\lancet-covid-19-database-_lZEB7Vl\lib\site-packages\pandas\core\generic.py", line 3167, in to_csv
    formatter.save()
  File "C:\Users\Finn Woelm\.virtualenvs\lancet-covid-19-database-_lZEB7Vl\lib\site-packages\pandas\io\formats\csvs.py", line 185, in save
    f, handles = get_handle()
  File "C:\Users\Finn Woelm\.virtualenvs\lancet-covid-19-database-_lZEB7Vl\lib\site-packages\pandas\io\common.py", line 493, in get_handle
    f = open(path_or_buf, mode, encoding=encoding, errors=errors, newline="")
PermissionError: [Errno 13] Permission denied: 'data\\database.csv'
```

This error occurs when python tries to update an indicator or the overall database, while the indicator (or overall database) file is open in Excel or another program on your computer.

To solve this issue, simply close all open files in Excel (or any other program you might use to open the database). Now, updating the datasets will succeed.

_Tip: You can see which file triggered the problem by looking at the line right above the error. In the case above, the error occurred just after it said `Rebuilding database...`, so we know that `database.csv` is open somewhere on the computer._

#### Other errors when updating the data

The datasets we extract could change at any time: new countries being added, the column names could change, the dataset format could change, the dataset could be moved to a new location. Any of these may break the current extraction code. There is no way to fix the extraction other than diving into the code and getting to the root of the problem.

Here is what such an error might look like:

```shell
Extracting indicator jhu_confirmed via pipeline jhu ...
Traceback (most recent call last):
  File ".\extract_indicator.py", line 40, in <module>
    run_pipeline(indicator)
  File "C:\Users\Finn Woelm\Projects\lancet-covid-19-database\pipelines\jhu.py", line 26, in run_pipeline
    data = data[['country', 'state']]
  File "C:\Users\Finn Woelm\.virtualenvs\lancet-covid-19-database-_lZEB7Vl\lib\site-packages\pandas\core\frame.py", line 2905, in __getitem__
    indexer = self.loc._get_listlike_indexer(key, axis=1, raise_missing=True)[1]
  File "C:\Users\Finn Woelm\.virtualenvs\lancet-covid-19-database-_lZEB7Vl\lib\site-packages\pandas\core\indexing.py", line 1254, in _get_listlike_indexer
    self._validate_read_indexer(keyarr, indexer, axis, raise_missing=raise_missing)
  File "C:\Users\Finn Woelm\.virtualenvs\lancet-covid-19-database-_lZEB7Vl\lib\site-packages\pandas\core\indexing.py", line 1304, in _validate_read_indexer
    raise KeyError(f"{not_found} not in index")
KeyError: "['country'] not in index"
```

If you encounter this scenario, please contact finn.woelm@unsdsn.org, so that we can investigate the issue and resolve the error.

It is possible to temporarily skip certain indicators from being updated. This is useful when you want to update all the other indicators, except for the broken one. For the broken indicator, the latest version of the extraction will remain available and will be included in the database, but the program will **not** attempt to update that indicator and you will avoid the error.

The way to do this is to give the indicator a value of `inactive` in the `update_frequency` column in the `codebook.csv` file. The `extract_indicator.py` code skips any extractions for indicators that are marked as `inactive`. Any other indicators will be extracted as usual.

To figure out which indicator to mark as inactive, look for the line right before the error. In the example above, it is `Extracting indicator jhu_confirmed via pipeline jhu ...`. This tells you that the error occurred while extracting the `jhu_confirmed` indicator. So this is the one that you need to mark as inactive.

The next time you run the code for updating the indicators, you will see the following line:

```shell
Inactive indicators: ['owid_total_cases_per_million']
```

This lets you know which indicators are currently marked as inactive and are being skipped.

### Pipelines

Pipelines are defined in `/pipelines`. The first segment of each indicator ID defines the pipeline to run. For example, requesting to update `jhu_confirmed` will trigger `/pipelines/jhu.py`.

### Testing

To test the extractions, run `pytest`. It invokes tests defined in the
`/tests` folder.
