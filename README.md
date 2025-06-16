## About

A Python script that converts addresses into geographical coordinates (longitude and latitude). Primary work is done by package: [geocoder](https://github.com/DenisCarriere/geocoder). For further details regarding features refer to ```pygeoconverter.py``` script.

**Benchmark**: In a single threaded mode it was possible to convert around 55K addresses into coordinates in 3 days (the script worked not more then 5-6 hours daily).

**NOTE**: Script should skip already converted locations. But be careful: interrupting script while working may remove already converted data (only from last "batch", which is also configurable). Thus, a `tar` file as a backup is created before a retrieve process launches.

## Structure

* **data** - contains initial CSV with addresses and retrieved results in various formats (Python dictionary + CSV)
* **pygeoconverter** - main Python script and configuration files
* **tests** - multiple test of other geo python packages (e.g., `geopy`, `googlemaps`,)

## Dependencies

* Python 3
* `requirements/requirements-prod.txt`

## Preparing

* Install dependencies
	- [scripts/cmdInitiateEnv.bat](scripts/cmdInitiateEnv.bat)
* (optional) create folder `data` and file `SampleDataSource.csv`
	```
	mkdir data
	cd data
	touch SampleDataSource.csv
	```

## Usage

In case there were no data downloaded before script will through exception first time. But on the second run should proceed successfully. For configurations use 'configs.py' file.

```
cd script
cmdStartEnv.bat
cd pygeoconverter
python pygeoconverter.py
```

## License

[LICENSE](LICENSE)
