# -*- coding: utf-8 -*-

####################
# Configuration file
####################

#
# SETTINGS
#

SLEEP_INTERVAL = 1
REQUESTS_PER_INTERVAL = 15
REQUESTS_BEFORE_BACKUP = 2*(SLEEP_INTERVAL*60)

PY_DB_MODULE = 'geodb'
PY_DB_MODULE_SKIPPED = 'geodb_skipped'

FOLDER = '../data/'
CSV_DELIMITER = ';'
#DATA_FILE = 'EEGAnlagenstammdaten.csv'
DATA_FILE = 'SampleDataSource.csv'

DATA_FILE_PATH = '{0}{1}'.format(FOLDER, DATA_FILE)

#
# HELPER FUNCTIONS
#

def load_data_from_py_module(module_name, module_path):
    """Load database of downloaded locations as a Python dictionary """

    import sys
    sys.path.insert(0, module_path)
    print ('[i] importing module {0}'.format(module_name))

    try:
        mod = __import__(module_name, fromlist=[''])
    except ImportError:
        print ('[i] creating new database under name {0}'.format(PY_DB_MODULE))
        save_data_as_pyobj({}, module_name)
        return None

    if module_name == PY_DB_MODULE:
        return mod.geodb

    if module_name == PY_DB_MODULE_SKIPPED:
        return mod.geodb_skipped

def save_data_as_pyobj(variable, variable_name, file_name=None):
    """Save variable as python object into file"""

    from pprint import pprint
    import codecs

    if file_name is None:
        file_name = '{0}{1}.py'.format(FOLDER, variable_name)

    _file = codecs.open(file_name, 'wb', 'utf8')
    _file.write('# -*- coding: utf-8 -*-\n')
    _file.write('{0} = '.format(variable_name))
    pprint(variable, stream=_file, indent=2)
    _file.close()

def save_db_as_csv(csv_file_name=None, delimiter=None):
    """ Save database as CSV """

    print ('[i] transformation of retrieved geo data into CSV file')

    if delimiter is None:
        delimiter = CSV_DELIMITER

    if csv_file_name is None:
        csv_file_name = '{0}{1}.csv'.format(FOLDER, PY_DB_MODULE)

    geo_database = load_data_from_py_module(PY_DB_MODULE, FOLDER)

    header = 'key{0}plz{0}plz3{0}latitude{0}longitude{0}address\n'.format(delimiter)
    csv = open(csv_file_name, 'w')
    csv.write(header)
    for key in geo_database:
        csv.write('{0}{1}'.format(geo_database[key]['key'], delimiter))
        csv.write('{0}{1}'.format(geo_database[key]['plz'], delimiter))
        csv.write('{0}{1}'.format(geo_database[key]['plz'][:3], delimiter))
        csv.write('"{0}"{1}'.format(geo_database[key]['location']['lat'], delimiter)) #latitude
        csv.write('"{0}"{1}'.format(geo_database[key]['location']['lng'], delimiter)) #longitude
        csv.write('"{0}"{1}'.format(geo_database[key]['address'], delimiter))
        csv.write('\n')

    csv.close()


