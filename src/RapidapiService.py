import requests

class RapidapiService():

    def __init__(self):
        self.url = "https://restcountries-v1.p.rapidapi.com/"
        self.headers = {
        'x-rapidapi-key': "78199a9fedmsh47e0058d12e41dep1bf329jsn22e6e03e973b",
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com"}

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