import importlib
import argparse

from config import INDICATORS
from helpers.glob_match import glob_match

# Set up program arguments
program = argparse.ArgumentParser(description = 'Extract one or more indicators.')

program.add_argument(
    'indicator',
    nargs = '+',
    help = 'the indicator to extract (you can use wildcards, like * and ?)'
)

# Get the arguments
args = program.parse_args()
indicator_globs = args.indicator

# Identify the indicators to extract
indicators = []
for item in INDICATORS:
    if any([glob_match(glob, item['id']) for glob in indicator_globs]):
        indicators.append(item)

# Run the pipeline for each indicator
for indicator in indicators:
    id = indicator['id']
    pipeline = indicator['pipeline']
    arguments = {k:v for k,v in indicator.items() if k not in ['id', 'pipeline']}

    print('Extracting indicator', id, 'via pipeline', pipeline, '...')

    # Load the pipeline
    module = importlib.import_module('.' + pipeline, 'pipelines')
    run_pipeline = getattr(module, 'run_pipeline')

    # Run the pipeline
    run_pipeline(id, **arguments)
    print('Extracting indicator', id, 'via pipeline', pipeline, '...', 'Done! :)')
