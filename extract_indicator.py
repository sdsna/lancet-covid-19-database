import importlib
import argparse

from config import PIPELINES

# Set up program arguments
program = argparse.ArgumentParser(description='Extract a single indicator.')

program.add_argument('indicator', help='the indicator to extract')

# Get the arguments
args = program.parse_args()
indicator = args.indicator

# TODO: Add support for regex pipelines: jhu*
#       and multiple pipelines: jhu_cases jhu_deaths

# Find the pipeline to run
pipeline = next(item for item in PIPELINES if item['indicator'] == indicator)
print('Extracting indicator', indicator, 'via pipeline', pipeline['pipeline'], end=' ... ')

# Load the pipeline
module = importlib.import_module('.' + pipeline['pipeline'], 'pipelines')
run_pipeline = getattr(module, 'run_pipeline')

# Run the pipeline
pipeline_args = {k:v for k,v in pipeline.items() if k not in ['indicator', 'pipeline']}
run_pipeline(pipeline['indicator'], **pipeline_args)
print("Done!")
