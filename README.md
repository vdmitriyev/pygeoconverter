### About

Converting openly accessible address locations  into geographical coordinates (longitude and latitude). Primary the work done with means of OSM. For further details regarding features refer to ```pygeoconverter.py``` script. I was able to download around 55 000 coordinates in 3 days (each day script worked not more then 5-6 hours and was also continuously improved).

**NOTE** Script should skip already downloaded locations. But be careful - interrupting script while working may remove already downloaded data (only from last "batch", which is also configurable). Because of this reason backup in form of 'tar' file is always created before launching retrieving process.

### Structure

* **data** - contains initial csv with addresses and resulting data (py dict + CSV)
* **pygeoconverter** - main Python script + configuration file
* **tests** - multiple test of other geo python libraries (e.g. Google Map)

### Dependencies

* Python 2.7
* geocoder

### Preparing

```
pip install geocoder
```

### Usage

In case there were no data downloaded before script will through exception first time. But on the second run should proceed successfully. For configurations use 'configs.py' file.

```
python pygeoconverter.py
```

