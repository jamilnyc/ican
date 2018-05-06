import json

import requests
from weather import Unit
from weather import Weather


class LocalWeather:
    """
    Weather service that retrieves the weather information of the current location.

    Public Methods:
        getCurrentGeoLocation()
        getCurrentConditionByGeoLocation()
        getCurrentTemperature()
    """

    weather = None
    location_url = "http://freegeoip.net/json"

    def __init__(self):
        self.weather = Weather(unit=Unit.FAHRENHEIT)

    def getCurrentGeoLocation(self):
        """
        Return a dictionary of current longitude and latitude based on IP address.
        :return: dictionary with fields "longitude" and "latitude"
        """
        r = requests.get(self.location_url)
        j = json.loads(r.text)
        return {
            'latitude': j['latitude'],
            'longitude': j['longitude'],
        }

    def getCurrentConditionByGeoLocation(self, latitude, longitude):
        """
        Return the current Yahoo Weather conditions of the given longitude and latitude.
        :param latitude: Location longitude as a number
        :param longitude: Location latitude as a number
        :return: Yahoo Weather condition object
        """
        lookup = self.weather.lookup_by_latlng(latitude, longitude)
        condition = lookup.condition
        return condition

    def getCurrentTemperature(self):
        """
        Return the temperature of the current location in Fahrenheit.
        :return: Fahrenheit temperature as a number
        """
        geo = self.getCurrentGeoLocation()
        condition = self.getCurrentConditionByGeoLocation(geo['latitude'], geo['longitude'])
        return condition.temp
