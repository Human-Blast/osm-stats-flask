import flask
from flask import request
from flask_restful import Api, Resource
import pyrebase
import datetime
import pandas as pd
import json
import os
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
api = Api(app)
countries =['brazil','india','china','south africa','russia']
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

            for date in dates.val():
                # for i in range(0,4):
                # print(json_dict[str(date)])
                df = pd.DataFrame(json_dict[str(date)])
                print(df)
            # print(dates.val())
            
            # print(json_dict['20140101']['frequency'])

            # df = pd.DataFrame.from_dict(json_dict,orient='index')
            # df.reset_index(level=0,inplace=True)
            # print(df)
            return "Check console"
        return "Invalid input"



api.add_resource(JSON_CSV,"/api/jsoncsv/<string:country>/<string:category>")
api.add_resource(CSV_file,"/api/download/<string:country>/<string:category>")
api.add_resource(CountryData, "/api/country/<string:name>/<string:category>")

if __name__ == "__main__":
    app.run(debug=True)
