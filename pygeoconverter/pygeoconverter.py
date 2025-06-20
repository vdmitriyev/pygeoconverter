__version__ = "1.1.0"
__description__ = (
    "Converting locations from open access data to longitude and latitude."
)

import os
import sys
import tarfile
import time
import traceback
import uuid
from datetime import datetime
from pprint import pprint
from time import sleep

import configs as configs
import geocoder
import helpers as helpers
from helpers import custom_print

# set 'True' for debugging (stdout will be more verbose)
DEBUG = False
VERIFY = True


class GeoConverter:

    def __init__(self):
        """Init method"""

        if DEBUG:
            custom_print('[i] class "GeoConverter" created')
        self.geo_database = {}
        self.unique_keys = {}
        self.proxies = {}

    def set_proxies(self, proxies: list):
        self.proxies = proxies

    def prepare_data(self):
        """Preparing data for work - loading and making backups"""

        self.make_db_backup()

        if not self.unique_keys:
            self.read_unique_keys()

        self.geo_database = helpers.load_data_from_py_module(
            configs.PY_DB_MODULE, configs.FOLDER
        )
        self.geo_database_skipped = helpers.load_data_from_py_module(
            configs.PY_DB_MODULE_SKIPPED, configs.FOLDER
        )

        # filtering non-solars
        # was a temporary hack
        # tmp = {}
        # for key in self.geo_database:
        #     if key in self.unique_keys:
        #         tmp[key] = self.geo_database[key]
        # pprint(tmp)

    def make_db_backup(self):
        """Making backup of downloaded db"""

        ts = time.time()
        prefix = "{0}-{1}".format(
            datetime.fromtimestamp(ts).strftime("%Y%m%d-%H%M%S"), str(uuid.uuid1())[:2]
        )
        archive_file_path = "{0}{1}-{2}.tar.gz".format(
            configs.FOLDER, prefix, configs.PY_DB_MODULE
        )
        custom_print("[i] making backup into file {0}".format(archive_file_path))
        tar = tarfile.open(archive_file_path, "w:gz")
        try:
            files = [
                "{0}{1}.py".format(configs.FOLDER, configs.PY_DB_MODULE),
                "{0}{1}.py".format(configs.FOLDER, configs.PY_DB_MODULE_SKIPPED),
            ]
            for file in files:
                if os.path.exists(file):
                    tar.add(file)
        except:
            custom_print("[i] nothing to backup")
        tar.close()

    def read_unique_keys(self):
        """Reading unique data from CSV"""

        csv = open(configs.DATA_FILE_PATH, "r")
        _ = csv.readline()  # ignoring first line

        results = {}
        # f_uniques = {}
        for line in csv:
            rows = line.split(configs.CSV_DELIMITER)
            # f_uniques[rows[5]] = 1
            if rows[5].upper() == "SOLAR":
                results[rows[0]] = {
                    "address": (
                        ",".join((rows[1], rows[2], rows[3], rows[4])).replace("#", "1")
                    ),
                    "plz": rows[2],
                    "key": rows[0],
                }
        # print(f_uniques)
        custom_print("[i] total unique keys {0}".format(len(results)))
        self.unique_keys = results
        csv.close()

        return results

    def statistics(self):
        """Gathering statistics about already processed data"""

        if len(self.geo_database) == 0:
            self.prepare_data()

        if self.geo_database is None or self.geo_database_skipped is None:
            print("\n[e] cannot read the database backup, restart the script")
            return False

        unique = len(self.unique_keys)
        properly_processed = len(self.geo_database)
        skipped_processed = len(self.geo_database_skipped)

        print("")
        custom_print(
            "[i] already processed data {0}".format(
                properly_processed + skipped_processed
            )
        )
        custom_print("[i] properly processed data {0}".format(properly_processed))
        custom_print("[i] skipped processed data {0}".format(skipped_processed))

        left_keys = unique - (properly_processed + skipped_processed)
        estimated_time_left = (left_keys / configs.REQUESTS_PER_INTERVAL) / 60.0
        custom_print("[i] more to go {0}".format(left_keys))
        custom_print("[i] estimated time in minutes {0}".format(estimated_time_left))
        custom_print(
            "[i] estimated time in hours {0}\n".format(estimated_time_left / 60.0)
        )

        return True

    def get_coordinates(self, address: str):
        """
        Using geocoder to decode address
            - can use various providers (Google, OSM, etc.) https://geocoder.readthedocs.org/
            - can output GeoJSON
        """

        is_retrieved, g_geocoder = False, None
        # try:
        #     # if len(self.proxies) != 0:
        #     #     g_geocoder = geocoder.osm(address, proxies=self.proxies)
        #     g_geocoder = geocoder.osm(address)
        #     if g_geocoder is not None and g_geocoder.latlng is not None:
        #         if g_geocoder.latlng != []:
        #             is_retrieved = True
        # except:
        #     is_retrieved = False
        #     print(traceback.format_exc())

        # in case OSM didn't provide anything use Google Maps
        try:
            if not is_retrieved:
                g_geocoder = geocoder.google(address)
            if g_geocoder is not None and g_geocoder.latlng is not None:
                if g_geocoder.latlng != []:
                    is_retrieved = True
        except:
            is_retrieved = False
            print(traceback.format_exc())

        # in case Google Maps didn't provide anything use ArcGIS
        try:
            if not is_retrieved:
                g_geocoder = geocoder.arcgis(address)
            if g_geocoder is not None and g_geocoder.latlng is not None:
                if g_geocoder.latlng != []:
                    is_retrieved = True
        except:
            is_retrieved = False
            print(traceback.format_exc())

        coordinates = []
        if g_geocoder is not None:
            coordinates = g_geocoder.latlng

        latitude, longitude = None, None
        if coordinates is not None and len(coordinates) == 2:
            latitude, longitude = coordinates[0], coordinates[1]
        else:
            print("[ex] wrong coordinates format")

        if DEBUG:
            custom_print("[i] location : {0} {1}".format(latitude, longitude))

        return {"lat": latitude, "lng": longitude}

    def process_unique_keys(self):
        """Processing unique keys in order to retrieve coordinates"""

        if len(self.geo_database) == 0:
            self.prepare_data()

        def save_data():
            self.make_db_backup()
            self.statistics()
            helpers.save_data_as_pyobj(self.geo_database, configs.PY_DB_MODULE)
            helpers.save_data_as_pyobj(
                self.geo_database_skipped, configs.PY_DB_MODULE_SKIPPED
            )

        for index, current_key in enumerate(self.unique_keys):
            # if DEBUG: print ('[i] checking key {0}'.format(current_key))
            if (
                current_key not in self.geo_database
                and current_key not in self.geo_database_skipped
            ):
                if DEBUG:
                    custom_print("[i] not yet retrieved {0}".format(current_key))
                address = self.unique_keys[current_key]["address"]
                try:
                    retrieved_location = self.get_coordinates(address)
                except Exception as ex:
                    if DEBUG:
                        print("[x] following key skipped {0}".format(current_key))
                    print("[ex] Exception: {0}".format(ex))
                    print(traceback.format_exc())
                    self.geo_database_skipped[current_key] = {"key": current_key}

                if current_key not in self.geo_database_skipped:
                    self.geo_database[current_key] = self.unique_keys[current_key]
                    self.geo_database[current_key]["location"] = retrieved_location

                if index % configs.REQUESTS_PER_INTERVAL == 0:
                    sleep(configs.SLEEP_INTERVAL)

                if index % configs.REQUESTS_BEFORE_BACKUP == 0:
                    save_data()

        save_data()


class Logger(object):

    def __init__(self):
        """Initializing log file with random name"""

        self.terminal = sys.stdout
        suffix = "{0}-{1}".format(
            datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M"),
            str(uuid.uuid1())[:2],
        )
        self.log = open("logfile-{0}.log".format(suffix), "a")

    def write(self, message):
        """Overriding writing method to write to file and stdout at once"""

        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        """flush method is needed for python 3 compatibility
        handles the flush command by doing nothing
        you might want to specify some extra behavior here
        """

        pass


def main():
    """Creates classes and runs process"""

    geo_converter = GeoConverter()
    if not geo_converter.statistics():
        exit(1)

    # geo_converter.make_db_backup()
    geo_converter.process_unique_keys()
    helpers.save_db_as_csv(delimiter=",")


if __name__ == "__main__":
    sys.stdout = Logger()
    main()
