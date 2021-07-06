from flask import Flask, session, request
from flask.templating import render_template
import os
import dbconn
import psycopg2 as sql

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/install")
def install():
    db = dbconn.connect().cursor()
    s

# 손님 명단 추출
@app.route("/customer/<customerID>", method=('GET'))
def customerList():
    db = dbconn.connect().cursor()
