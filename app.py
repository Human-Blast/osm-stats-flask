import flask
from flask import request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
from pandas import *
import json
import os

app = flask.Flask(__name__)
cred = credentials.Certificate('open-street-map-research-firebase-adminsdk-4kv8q-3f47cae2b0.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://open-street-map-research-default-rtdb.firebaseio.com'})


@app.route('/',methods=['GET'])

def home():
    ref = db.reference('osm-data/analyzed/india/top_5/data')
    return ref.get()