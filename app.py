from flask import Flask
from os import getenv
import csv

with open('static/birdnames.csv', mode='r') as csvfile:
    birdlist = [bird[0] for bird in csv.reader(csvfile)]


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes

