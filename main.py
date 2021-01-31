import os
import pandas as pd
import webbrowser

from src.RapidapiService import RapidapiService
from src.CountriesService import CountriesService
from src.Db import Db

def main():

    # Get all the regions
    regions = getRegions()
    # Get all the cities with it's language
    cities = getCities(regions)
    # Generate the dataframe
    df = createDataFrame(cities)
    # show statistics
    sdf = statistics(df)
    # Display the dataframe as a HTML file
    displayDataframe(df, sdf)
    # Save the dataframe into SQLite
    saveDB(df)
    # Save the dataframe in a JSON file
    datasetToJson(df)

def getRegions():
    # Create the service's object
    obj_regions = RapidapiService()
    # Get all the regions
    regions = obj_regions.getRegions()
    return regions
    

def getCities(regions):   
    data = {"Region": [], "City": [], "Language": [], "Time": []}
    # Create Service's object
    obj_countries =  CountriesService()
    # Get three cities
    for region in regions["Region"]:
        # Get Country
        response = obj_countries.getCountryByRegion(region, params={"fields":"name;languages"})
        # Get the data
        data["Region"].append(region)
        data["City"].append(response["City"])
        data["Language"].append(response["Language"])
        data["Time"].append(float(response["Time"])+float(regions["Time"])) 

    return data

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