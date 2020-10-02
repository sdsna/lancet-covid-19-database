import pandas
from config import CODEBOOK_PATH

codebook = pandas.read_csv(CODEBOOK_PATH)

# Return indicator IDs from codebook
def get_indicator_ids():
    return list(codebook["indicator"])


# Return inactive indicator IDs from codebook
def get_inactive_indicator_ids():
    inactive = codebook[codebook["update_frequency"] == "inactive"]
    return list(inactive["indicator"])


# Return active indicator IDs from codebook
def get_active_indicator_ids():
    active = codebook[codebook["update_frequency"] != "inactive"]
    return list(active["indicator"])
