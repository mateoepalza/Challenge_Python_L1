import pandas as pd
import hashlib
import datetime
from src.Restful import Restful 
from src.connection import Db

def main():
    
    time = getTime()
    regions = getRegions()
    cities = getCities(regions.get('Region'), time)
    regions.update(cities)
    df = createDataFrame(regions)
    stadistics(df)
    saveDB(df)
    datasetToJson(df)

def getTime():
    return datetime.datetime.utcnow()

def getRegions():

    regions = {"Region" : []}

    obj =  Restful("https://restcountries-v1.p.rapidapi.com/")

    result = obj.get("all",{
        'x-rapidapi-key': "78199a9fedmsh47e0058d12e41dep1bf329jsn22e6e03e973b",
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com"}
        )

    # Get the regions
    for country in result:
        if str.lower(country.get('region')) not in regions.get("Region") and country.get('region') != "":
            regions.get("Region").append(str.lower(country.get('region')))
    
    return regions

def getCities(regions, time):   
    cities = {"city": [], "Language": [], "Time": []}
    # Update the URL
    obj = Restful("https://restcountries.eu/rest/v2/")

    # Get three cities
    for region in regions:

        res = obj.get('region/'+region, params={"fields": "name;languages"})
        if len(res) > 0:
            # Select the first city
            city = res[0]
            # store the city inside the list
            cities.get("city").append(city.get('name'))
            #cities.get("Language").append(hashlib.new("hash", (city.get('languages')[0]).get('name').encode('utf-8')))
            cities.get("Language").append((city.get('languages')[0]).get('name'))
            cities.get("Time").append((datetime.datetime.utcnow() - time).total_seconds())

    return cities

def createDataFrame(data):
    df = pd.DataFrame(data)
    print(df)
    return df

def stadistics(df):
    # Convert to numeric
    df["Time"].describe()
    print()
    print("Tiempo total")
    print(df["Time"].sum())
    print("Tiempo promedio")
    print(df["Time"].mean())
    print("Tiempo mínimo")
    print(df["Time"].min())
    print("Tiempo máximo")
    print(df["Time"].max())
    
def saveDB(df):
    # Create connection
    database = Db()
    #database.createDataBase()
    # Save dataframe
    database.saveDataframe(df, "Region")
    # Close connection
    database.closeConnection()


def datasetToJson(df):
    df.to_json("JSON/dataframe.json")

if __name__ == "__main__":
    main()