# Lancet Data Extractions

## Data

You can find the full database, codebook, and indicator files in [the `/data/` folder](https://github.com/sdsna/lancet-data/tree/master/data).

---

## Development Notes

The extraction code is written in Python.

### Updating Datasets

To update all datasets, run:

```shell
python extract_indicator.py *
```

To update a specific dataset, run:

```shell
python extract_indicator.py jhu-cases
```

You can use wildcards (`*` and `?`) to extract several indicators at once:

```shell
python extract_indicator.py owid*
```

### Pipelines

Pipelines are defined in `/pipelines`. The first segment of each indicator ID defines the pipeline to run. For example, requesting to update `jhu_confirmed` will trigger `/pipelines/jhu.py`.

### Testing

To test the extractions, run `pytest`. It invokes tests defined in the
`/tests` folder.
