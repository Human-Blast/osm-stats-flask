import flask
from flask import request
from flask_restful import Api, Resource
from flask_cors import CORS
import pyrebase
import datetime
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from DataRetrieve import *
from ImageProcess import *
from helper_functions import *


firebaseConfig = {
    "apiKey": "AIzaSyBTzzXFHncci7RanGMjNfduJ8_471RkYoU",
    "authDomain": "open-street-map-research.firebaseapp.com",
    "databaseURL": "https://open-street-map-research-default-rtdb.firebaseio.com",
    "storageBucket": "open-street-map-research.appspot.com",
    "serviceAccount": "open-street-map-research-firebase-adminsdk-4kv8q-3f47cae2b0.json"
     }

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
store = firebase.storage()
app = flask.Flask(__name__)
CORS(app)
api = Api(app)
countries =['brazil','india','china','southafrica','russia']
category_ = ['building','leisure','amenity','office','man_made','advertising','shop','craft','historic','landuse','tourism','boundary']

class CountryData(Resource):
    def get(self, name,category):
        name = name.lower()
        category = category.lower()
        if(name in countries and category in category_):
            return "Valid Country and Category. Use POST request to get the DATA"
        return "Invalid Data.Check the docs for the API usage"

    def post(self, name,category):

        name = name.lower()
        category = category.lower()
        
        if (name in countries):
            if(category == 'all'):
                country_data = db.child('/osm_data/analyzed/'+name+'/top_5/data').get()
                # print("Country data is "+ name)
                return country_data.val()
            else:
                if(category in category_):
                    category_index = category_.index(category)
                    category_data = db.child('/osm_data/analyzed/'+name+'/top_5/data/'+str(category_index)+'/'+category).get()
                    # print(category_data.val())
                    return category_data.val()  

        return "Invalid Data.Check the docs for the api usage" 

class CSV_file(Resource):
    def get(self,country,category):
        country = country.lower()
        category = category.lower()
        if(country in countries and category in category_):
           download_csv(country,category)
           return "Download Successsful"
        return "Invalid Data.Check the docs for the API usage"

class JSON_CSV(Resource):
    def get(self,country,category): 
        country = country.lower()
        category = category.lower() 
        if(country in countries and category in category_):
            category_index = category_.index(category)
            category_data = db.child('/osm_data/analyzed/'+country+'/top_5/data/'+str(category_index)+'/'+category).get()
            json_dict = category_data.val()
            dates = db.child('/osm_data/dates/'+country).get()

            dfs_created = []
            years = dates.val()

            for date in years:
                # for i in range(0,4):
                # print(json_dict[str(date)])
                df_name = country +'_'+ category
                column_for_tag = category +'_'+ str(date)
                globals()[df_name] = pd.DataFrame(json_dict[str(date)],index=[str(date) for i in range(5)])
                dfs_created.append(globals()[df_name])
            
            if len(dfs_created) > 0:
                merge_df  = pd.concat(dfs_created) #.fillna(0).sort_values(df_column)
                x = Data_Manipulation(merge_df, years, category, country)
                fig = x.RefineData_and_GenerateGraph('bar')
                # print(type(fig))
                # file_name = 'test.svg'
                # plt.savefig(file_name, dpi=100) 
                img = ImageProcess(fig)
                return img.ImageToBase64()
            else:
                return "error obtaining graph image"

        return "Invalid input"


# monthly data of osm
api.add_resource(JSON_CSV,"/api/pygraph/<string:country>/<string:category>")
api.add_resource(CSV_file,"/api/download/<string:country>/<string:category>")
api.add_resource(CountryData, "/api/country/<string:name>/<string:category>")

if __name__ == "__main__":
    app.run(debug=True)
