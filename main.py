import os
import pandas as pd
import hashlib
import datetime
import webbrowser
from src.Restful import Restful 
from src.connection import Db

def main():
    
    # Get the current time
    time = getTime()
    # Get all the regions
    regions = getRegions()
    # Get all the cities with it's language
    cities = getCities(regions.get('Region'), time)
    # Generate the full dictionary
    regions.update(cities)
    # Generate the dataframe
    df = createDataFrame(regions)
    # show statistics
    sdf = statistics(df)
    # Display the dataframe as a HTML file
    displayDataframe(df, sdf)
    # Save the dataframe into SQLite
    saveDB(df)
    # Save the dataframe in a JSON file
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
            cities.get("Time").append(float("{0:.3f}".format((datetime.datetime.utcnow() - time).total_seconds())))

    return cities

def createDataFrame(data):
    # Generate the data frame using the dictionary
    return pd.DataFrame(data)

def statistics(df):
    # Generate statistics
    stad = {"Tiempo mínimo": ["{0:.3f}".format(df["Time"].min())+" s"], "Tiempo máximo": ["{0:.3f}".format(df["Time"].max())+" s"], "Tiempo promedio": ["{0:.3f}".format(df["Time"].mean())+" s"], "Tiempo total": ["{0:.3f}".format(df["Time"].sum())+" s"]}
    return pd.DataFrame(stad)

def displayDataframe(df, sdf):
    # Get path of the file
    dataframe_path = os.path.join(os.getcwd(), "src", "dataframe", "index.html")
    # Open the file
    f = open(dataframe_path,"w+")
    # Write the table's HTML
    f.write(getHtml(df, sdf))
    # Close the file
    f.close()
    # Open in the browser
    webbrowser.open(dataframe_path)

def getHtml(df, sdf):
    body = f"""
        <html>
            <head>
                <link rel ='stylesheet' href='css/index.css'>
            </head>
            <body>
                <div class='container'>
                    <div>
                            <h2 class='title'>Regions</h2>
                            <div class='tables main-table'>
                                {df.to_html()}
                            </div>
                    </div>
                    <div>
                            <h2 class='title'>Statistics</h2>
                            <div class='tables second-table'>
                                {sdf.to_html()}
                            </div>
                    </div>
                </div>
            </body>
        </html>"""

    return body

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