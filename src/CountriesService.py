import requests
import hashlib


class CountriesService():

    def __init__(self):

        self.url = "https://restcountries.eu/rest/v2/"
        self.headers = {}

    def getCountryByRegion(self, region, params={}):
        cities = {"City": "", "Language": "","Time": ""}
        # Request
        response = requests.get(self.url+'region/'+region, params=params, headers=self.headers)
        # Parse
        result = response.json()
        # Select the first city
        city = result[0]
        # store the city inside the list
        cities["City"] = city.get('name')
        # Get the language
        #cities.get("Language").append(hashlib.new("hash", (city.get('languages')[0]).get('name').encode('utf-8')))
        cities["Language"] = (city.get('languages')[0]).get('name')
        # Get the time of the request
        cities["Time"] = response.elapsed.total_seconds()

        return cities
