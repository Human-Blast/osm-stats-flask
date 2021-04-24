import flask
from flask import request
from flask_restful import Api, Resource

import pyrebase
import datetime
from pandas import *
import json
import os

firebaseConfig = {
    "apiKey": "AIzaSyBTzzXFHncci7RanGMjNfduJ8_471RkYoU",
    "authDomain": "open-street-map-research.firebaseapp.com",
    "databaseURL": "https://open-street-map-research-default-rtdb.firebaseio.com",
    "storageBucket": "open-street-map-research.appspot.com",
    "serviceAccount": "open-street-map-research-firebase-adminsdk-4kv8q-3f47cae2b0.json"
     }

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
app = flask.Flask(__name__)
api = Api(app)
class CountryData(Resource):
    def get(self, name):
        return {"country": name, "request": "GET"}

    def post(self, name):
        country_data = db.child('/osm_data/analyzed/'+name+'/top_5/data').get()
        print("Country data is "+ name)
        return country_data.val()

class Active(Resource):
    def post(self):
        return "active"

api.add_resource(CountryData, "/api/country/<string:name>")
api.add_resource(Active,"/")


if __name__ == "__main__":
    app.run(debug=False)


# @app.route('/api/get_data',methods=['GET','POST'])
# def get_data():
#     ref = db.reference('osm-data/analyzed/india/top_5/data')
#     # return ref.get()
#     if request.method == 'POST':
