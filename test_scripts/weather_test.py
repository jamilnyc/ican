import sys

sys.path.append('../src/api')
import local_weather

w = local_weather.LocalWeather()
geo = w.getCurrentGeoLocation()
print geo

temp = w.getCurrentTemperature()
print temp