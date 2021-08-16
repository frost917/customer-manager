from flask import Flask, session, request, jsonify
import flask
from flask.templating import render_template
import json
import os
import dbconn
import psycopg2 as sql

app = Flask(__name__)
app.secret_key = os.urandom(32)

# @app.route("/install")
# def install():
#     db = dbconn.connect().cursor()
#     s

@app.route("/", method=['GET', 'POST'])
def index():
    return """{}"""

@app.route("/login/<userID>", method=['GET', 'POST'])
def login():
    if request.method == "POST":
        userID = request.form.get('userID')
        password = request.form.get('passwd')
        originPasswordTuple = dbconn.Database.userPasswdComp(
            userID=userID)
        
        if originPasswordTuple is None:
            loginFailed = jsonify({"failed": ["location": "body","userID": userID,"error": "NoUser","msg": "user not found!"]})
            loginReturn = flask.Response(loginFailed, status=400, mimetype="application/json")
            return loginReturn
        
        uuidTuple = dbconn.Database.getUUID(
            userID=userID, passwd=password)

        if originPasswordTuple[1] == password:
             loginSuccessed = jsonify({
                "userID": userID,
                "UUID": uuidTuple[2]})
            loginReturn = flask.Response(loginSuccessed, status=200, mimetype="application/json")
            return loginReturn
        elif originPasswordTuple[1] != password:
            loginFailed = jsonify({
                "failed": [
                    "location": "body",
                    "userID": userID,
                    "error": "PasswordNotMatch",
                    "msg": "password is not matched!"
                ]
            })
            return loginFailed, 400

# 손님 명단 추출
# @app.route("/customer/<UUID>", method=['POST'])
# def customerList():
    

# if __name__ == "__main__":