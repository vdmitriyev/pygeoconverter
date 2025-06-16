####################
# CONFIGURATION FILE
####################

SLEEP_INTERVAL = 1
REQUESTS_PER_INTERVAL = 15
REQUESTS_BEFORE_BACKUP = 2 * (SLEEP_INTERVAL * 60)

PY_DB_MODULE = "geodb"
PY_DB_MODULE_SKIPPED = "geodb_skipped"

FOLDER = "../data/"
CSV_DELIMITER = ";"
# DATA_FILE = 'EEGAnlagenstammdaten.csv'
DATA_FILE = "SampleDataSource.csv"

DATA_FILE_PATH = "{0}{1}".format(FOLDER, DATA_FILE)
