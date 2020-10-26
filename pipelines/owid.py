import importlib

# Identify the correct pipeline to run
def run_pipeline(indicator):
    if indicator.find("_excess_mortality_") != -1:
        pipeline = "owid_excess_mortality"
    else:
        pipeline = "owid_database"
    print(">", "using sub-pipeline", pipeline, "...")

    # Load the pipeline
    module = importlib.import_module(".owid_pipelines." + pipeline, package=__package__)
    run_module_pipeline = getattr(module, "run_pipeline")

    # Run the pipeline
    run_module_pipeline(indicator)
