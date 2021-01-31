import requests

class Restful ():

    # Constructor
    def __init__(self, url):
        self.url = url

    # Methods
    def get(self, end_point, headers = {}, params = {}):

        response = requests.get(
            self.url+end_point,
            params = params,
            headers = headers
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None

