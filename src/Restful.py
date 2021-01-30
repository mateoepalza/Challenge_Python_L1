import requests

class Restful ():

    # Constructor
    def __init__(self, url):
        self.url = url
    
    # Getters
    #@property
    #def url(self):
    #    return self._url

    #@property
    #del end_point(self):
    #    return self.end_point

    #@property
    #del headers(self):
    #    return self.headers


    # Setters
    #@url.setter
    #def url(self, url):
    #    self._url = url

    #@end_point.setter
    #def end_point(self, end_point):
    #    self.end_point = end_point
    
    #@headers.setter
    #def url(self, headers):
    #    self.headers = headers


    # Methods
    def get(self, end_point, headers = {}, params = {}):
        print(self.url+end_point)
        response = requests.get(
            self.url+end_point,
            params = params,
            headers = headers
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None

