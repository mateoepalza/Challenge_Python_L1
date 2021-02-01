import requests
import os



class RapidapiService():

    def __init__(self):
        self.url = os.getenv("RPDP_HOST")
        self.headers = {
        'x-rapidapi-key': os.getenv("RPDP_KEY"),
        'x-rapidapi-host': os.getenv("RPDP_HEADER")
        }

    def getRegions(self, params={}):

        # Request
        response = requests.get(self.url+'all', params = params, headers = self.headers)
        # Parse
        result = response.json()
        # Regions
        regions = {"Region" : [], "Time": (response.elapsed.total_seconds())}
        # Get the regions
        for country in result:
            if str.lower(country.get('region')) not in regions.get("Region") and country.get('region') != "":
                regions.get("Region").append(str.lower(country.get('region')))
        
        return regions