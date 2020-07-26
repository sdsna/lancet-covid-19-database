import importlib
import argparse

from build_database import build_database
from helpers.glob_match import glob_match
from helpers.get_indicator_ids import get_indicator_ids

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
for indicator_id in get_indicator_ids():
    if any([glob_match(glob, indicator_id) for glob in indicator_globs]):
        indicators.append(indicator_id)

# Run the pipeline for each indicator
for indicator in indicators:
    pipeline = indicator.split('_')[0]

    print('Extracting indicator', indicator, 'via pipeline', pipeline, '...')

    # Load the pipeline
    module = importlib.import_module('.' + pipeline, 'pipelines')
    run_pipeline = getattr(module, 'run_pipeline')

    # Run the pipeline
    run_pipeline(indicator)
    print('Extracting indicator', indicator, 'via pipeline', pipeline, '...', 'Done! :)')

# Rebuild the database
print('Rebuilding database', '...')
build_database()
print('Rebuilding database', '...', 'Done! :)')
