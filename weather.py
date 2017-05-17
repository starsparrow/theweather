#!/usr/bin/env python

import sys
import requests


# Global variables

DARK_SKY_API_BASE_URL = 'https://api.darksky.net/forecast'
DARK_SKY_API_KEY = 'xxxxx'
ATTRIB = 'Powered by Dark Sky (https://darksky.net/poweredby)'
GOOGLE_MAPS_API_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'


# Class definitions

class Forecast:
    def __init__(self, loc, units='us'):
        payload = {'units': units}
        r = requests.get(
            '{api}/{key}/{location}/{time}'.format(api=DARK_SKY_API_BASE_URL,
                                                   key=DARK_SKY_API_KEY,
                                                   location=loc[0],
                                                   time=''),
            params=payload
        ).json()
        self.current_forecast = r['currently']
        self.current_summary = self.current_forecast['summary']
        self.current_temp = self.current_forecast['apparentTemperature']
        self.forecast_area = loc[1]
    
    def __str__(self):
        return '\nCurrent conditions for {}:\
                \nSummary:\t{}\
                \nTemperature:\t{}\
                \n\n{}'.format(self.forecast_area,
                                           self.current_summary,
                                           self.current_temp,
                                           ATTRIB)


class Location:
    def __init__(self, query):
        loc_data = requests.get(GOOGLE_MAPS_API_BASE_URL,
                                params={'address': query}).json()
        if loc_data['status'] not in ['INVALID_REQUEST', 'ZERO_RESULTS']:
            coords = loc_data['results'][0]['geometry']['location']  
            self.latlng = '{},{}'.format(coords['lat'], coords['lng'])
            self.formatted_address = loc_data['results'][0]['formatted_address']
        else:
            raise ValueError('Your search parameter was invalid or returned \
zero results. Please try again!')

    def __str__(self):
        return self.latlng
        

# Main section

if len(sys.argv) == 2:
    l = Location(sys.argv[1])
    print(Forecast((l.latlng, l.formatted_address)))
else:
    print('Please specify a single location (address, ZIP code, etc.) as an \
argument to this script. \nUse quotes for locations with spaces.')
