# Lancet Data Extractions

## Data

You can find the full database, codebook, and indicator files in [the `/data/` folder](https://github.com/sdsna/lancet-data/tree/master/data).

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
git clone https://github.com/sdsna/lancet-data.git
cd ./lancet-data/
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

To update all datasets, run:

```bash
python extract_indicator.py *
```

To update a specific dataset, run:

```bash
python extract_indicator.py jhu_cases
```

You can use wildcards (`*` and `?`) to extract several indicators at once:

```bash
python extract_indicator.py owid*
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

### Pipelines

Pipelines are defined in `/pipelines`. The first segment of each indicator ID defines the pipeline to run. For example, requesting to update `jhu_confirmed` will trigger `/pipelines/jhu.py`.

### Testing

To test the extractions, run `pytest`. It invokes tests defined in the
`/tests` folder.
