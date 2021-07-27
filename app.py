import flask
from flask import request
from flask_restful import Api, Resource
from flask_cors import CORS
import datetime
import pandas as pd
import json
import os
from DataProcess import *
from helper_functions import *
from DataAccess import *


db = FirebaseAuthentication().run_db()


app = flask.Flask(__name__)
CORS(app)
api = Api(app)

countries = db.child('/countries').get().val()
category_ = db.child('/categories').get().val()

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
        try:
            da = DataAccess(db, country = country, category = category, countriesInDB = countries, categoriesInDB = category_)
            img = da.GenerateAndSendDataTo_DataProcess('bar')

            if img == None:
                return "Invalid Request"

            return img

        except Exception:
            # return "Invalid Request"
            return Exception

class GetData_Year(Resource):
    def get(self,country,category,year):
        try:
            da = DataAccess(db, country = country, category = category, countriesInDB = countries, categoriesInDB = category_, allYears = year)
            img = da.GenerateAndSendDataTo_DataProcess('bar', top10=True)
            
            if img == None:
                return "Invalid Request"

            return img

        except Exception:
            return Exception
    

class GetCount(Resource):
    def get(self,country,category):
        # country = country.lower()
        # category = category.lower() 
        # dates = db.child('/osm_data/dates/'+country).get()
        # if(country in countries and category in category_ ):
        #     category_data = db.child('/osm_data/analyzed/'+country+'/count_top_10/'+category).get()
        #     # insert you code here
        #     df = pd.DataFrame(category_data.val())
        #     # print(df)
        #     return category_data.val()
        
        # return 'Inavlid data'
        try:
            da = DataAccess(db, country = country, category = category, countriesInDB = countries, categoriesInDB = category_)
            img = da.GenerateAndSendDataTo_DataProcess('scatter', scatterTop10=True)
            # print("-------------ooga buga return came-----------")
            if img == None:
                return "Invalid Request"

            return img

        except Exception:
            return Exception

class DB_Data(Resource):
    def get(self):
        try:
            category_data = db.child('/osm_data/all_data/analyzed/').get()
            return category_data.val()
        except Exception:
            return Exception
class DB_Data_Country(Resource):
    def get(self,country):
        try:
            country = country.lower()
            if(country in countries):
               category_data = db.child('/osm_data/all_data/analyzed/'+country).get()

            return category_data.val()
        except Exception:
            return Exception
class DB_Data_Category(Resource):
    def get(self,country,category):
        try:
            country = country.lower()
            category = category.lower() 
            category_index = category_.index(category)
            # dates = db.child('/osm_data/dates/'+country).get()
            if(country in countries and category in category_ ):
               category_data = db.child('/osm_data/all_data/analyzed/'+country+'/data/'+str(category_index)+'/'+category).get()

            return category_data.val()
        except Exception:
            return Exception


class DB_Data_Year(Resource):
    def get(self,country,category,year):
        try:
            country = country.lower()
            category = category.lower() 
            category_index = category_.index(category)
            if(country in countries and category in category_ ):
               category_data = db.child('/osm_data/all_data/analyzed/'+country+'/data/'+str(category_index)+'/'+category+'/'+str(year)).get()

            return category_data.val()
        except Exception:
            return Exception
        
# Graph data
api.add_resource(GetCount,"/osmapi/countgraph/<string:country>/<string:category>")
api.add_resource(GetData_Year,"/osmapi/pygraph/<string:country>/<string:category>/<int:year>")
api.add_resource(JSON_CSV,"/osmapi/pygraph/<string:country>/<string:category>")
api.add_resource(CSV_file,"/osmapi/download/<string:country>/<string:category>")


# Raw Data From DB
api.add_resource(DB_Data,"/osmapi/data")
api.add_resource(DB_Data_Country,"/osmapi/data/<string:country>")
api.add_resource(DB_Data_Category,"/osmapi/data/<string:country>/<string:category>")
api.add_resource(DB_Data_Year,"/osmapi/data/<string:country>/<string:category>/<int:year>")

if __name__ == "__main__":
    app.run(debug=True)
