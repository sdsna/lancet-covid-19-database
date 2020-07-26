import pandas
from config import CODEBOOK_PATH

codebook = pandas.read_csv(CODEBOOK_PATH)

# Return indicator IDs from codebook
def get_indicator_ids():
    return list(codebook['indicator'])
