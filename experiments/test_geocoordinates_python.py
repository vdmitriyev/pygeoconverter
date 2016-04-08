#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

import googlemaps
import geocoder
from geopy.geocoders import Nominatim

"""
Python geocoders clients comparison - http://webgeodatavore.com/python-geocoders-clients-comparison.html
"""

def test_googlemaps(address, method_name='googlemaps'):
    """ googlemaps """

    key_google_geo = 'AIzaSyCLISiRQmz5X2HlxTZZBpm21i_hIt4D30o'
    location = 'Abser Deich 8;26935;Stadland;Niedersachsen'.replace(';', ', ')

    gmaps = googlemaps.Client(key=key_google_geo)

    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    #print (pprint(geocode_result))

    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']
    print ('{0}\t{1} {2}'.format(method_name, latitude, longitude))

def test_geopy(address, method_name='geopy'):
    """ geopy
            - by default uses OSM OpenStreetMap (Nominatim)
            - supports more provides;
    """

    geolocator = Nominatim()
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    print ('{0}\t\t{1} {2}'.format(method_name, latitude, longitude))

def test_geocoder(address, method_name='geocoder'):
    """ geocoder
            - can use various providers (Google, OSM, etc.) https://geocoder.readthedocs.org/
            - can output GeoJSON
    """

    #g_geocoder = geocoder.google(address)
    g_geocoder = geocoder.osm(address)

    if g_geocoder.latlng == []:
        g_geocoder = geocoder.google(address)

    if g_geocoder.latlng == []:
        g_geocoder = geocoder.arcgis(address)

    if g_geocoder.latlng == []:
        g_geocoder = geocoder.yahoo(address)

    (latitude, longitude) = g_geocoder.latlng
    print ('{0}\t{1} {2}'.format(method_name, latitude, longitude))
    print(pprint(g_geocoder.geojson))

def run(from_file=False):
    """ Running scripts methods """

    #test_address = 'Abser Deich 8;26935;Stadland;Niedersachsen'.replace(';', ', ')
    #test_address = 'Friedrichsgrode 21;26409;Wittmund;Niedersachsen;'.replace(';', ', ')
    #test_address = 'Sandel 65 z;26441;Jever;Niedersachsen;'.replace(';', ', ')
    #test_address ='Rosa-Luxemburg- 5,28876,Oyten,Niedersachsen'
    #test_address = 'Neuheede Siedlu 999;26892;Heede;Niedersachsen'.replace(';', ', ')
    test_address = 'Achtern Buschho #;27367;Ahausen;Niedersachsen'.replace(';', ', ').replace('#', '1')
    print ('[i] following location will be checked:\n{0}'.format(test_address))
    print('method latitude longitude \n')

    #test_geopy(test_address)
    #test_googlemaps(test_address)
    test_geocoder(test_address)

if __name__ == '__main__':
    run()
