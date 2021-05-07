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

countries =['brazil','india','china','southafrica','russia']
category_ = ['building','leisure','amenity','office','man_made','advertising','shop','craft','historic','landuse','tourism','boundary']

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
            da = DataAccess(db, country, category, countries, category_)
            img = da.GenerateAndSendDataTo_DataProcess('bar')

            return img

        except Exception:
            # return "Error occured"
            return Exception

class GetData_Year(Resource):
    def get(self,country,category,year):
        country = country.lower()
        category = category.lower() 
        dates = db.child('/osm_data/dates/'+country).get()
        
        if(country in countries and category in category_ and year in dates.val()):
            category_index = category_.index(category)
            category_data = db.child('/osm_data/analyzed/'+country+'/top_10/data/'+str(category_index)+'/'+category+'/'+str(year)).get()
            json_dict = category_data.val()
            df = pd.DataFrame(json_dict,index=[str(year) for i in range(len(json_dict['frequency']))])

            #send em to the ranch
            x = Data_Manipulation(data = df, years= [year], category= category, country=country)
            img = x.RefineData_and_GenerateGraph(plot_kind = 'bar')

            return img
            
        return "Invalid Request"

class GetCount(Resource):
    def get(self,country,category):
        country = country.lower()
        category = category.lower() 
        dates = db.child('/osm_data/dates/'+country).get()
        if(country in countries and category in category_ ):
            category_data = db.child('/osm_data/analyzed/'+country+'/count_top_10/'+category).get()
            # insert you code here
            
            return category_data.val()
        
        return 'Inavlid data'

        
# monthly data of osm
api.add_resource(GetCount,"/osmapi/countgraph/<string:country>/<string:category>")
api.add_resource(GetData_Year,"/osmapi/pygraph/<string:country>/<string:category>/<int:year>")
api.add_resource(JSON_CSV,"/osmapi/pygraph/<string:country>/<string:category>")
api.add_resource(CSV_file,"/osmapi/download/<string:country>/<string:category>")


if __name__ == "__main__":
    app.run(debug=True)
