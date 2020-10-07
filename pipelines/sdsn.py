import importlib

# Identify the correct pipeline to run
def run_pipeline(indicator):
    if indicator == "sdsn_overall_transmission":
        pipeline = "sdsn_overall_transmission"
    else:
        pipeline = "sdsn_smoothed"
    print(">", "using sub-pipeline", pipeline, "...")

    # Load the pipeline
    module = importlib.import_module(".sdsn_pipelines." + pipeline, package=__package__)
    run_module_pipeline = getattr(module, "run_pipeline")

    # Run the pipeline
    run_module_pipeline(indicator)
