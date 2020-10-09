import importlib

# Indicators with a dedicated pipeline
DEDICATED_PIPELINES = [
    "overall_transmission",
]

# Identify the correct pipeline to run
def run_pipeline(indicator):
    if indicator.replace("sdsn_", "") in DEDICATED_PIPELINES:
        pipeline = indicator
    else:
        pipeline = "sdsn_smoothed"
    print(">", "using sub-pipeline", pipeline, "...")

    # Load the pipeline
    module = importlib.import_module(".sdsn_pipelines." + pipeline, package=__package__)
    run_module_pipeline = getattr(module, "run_pipeline")

    # Run the pipeline
    run_module_pipeline(indicator)
