import importlib
import argparse

from build_database import build_database
from make_badges import make_badges
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
all_indicator_ids = get_indicator_ids()
for indicator_id in all_indicator_ids:
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

# Rebuild badges
print('Remaking badges', '...')
is_full_extraction = len(indicators) == len(all_indicator_ids)
make_badges(full_extraction = is_full_extraction)
print('Remaking badges', '...', 'Done! :)')
