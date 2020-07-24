import importlib
import argparse

# Set up program arguments
program = argparse.ArgumentParser(description='Run a single pipeline.')

program.add_argument('pipeline', help='the pipeline to run')

# Get the arguments
args = program.parse_args()
pipeline = args.pipeline

# Run the pipeline
print("Running pipeline: " + pipeline, end=' ... ')
importlib.import_module('.' + pipeline, 'pipelines')
print("Done!")
