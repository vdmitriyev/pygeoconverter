### About

Converting openly accessible address locations  into geographical coordinates (longitude and latitude). Primary the work done with means of OSM. For further details regarding features refer to ```pygeoconverter.py``` script.

**NOTE** Script should skip already downloaded locations. But be careful - interrupting script while it's work may remove already downloaded data. Because of this reason backup in form of 'tar' file is always created before launching retrieving process.

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

In case there were no data downloaded before script will through exception first time. but on the second run should proceed successfully.

```
python pygeoconverter.py
```

