from flask import Flask, session, request, jsonify
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
            userID=userID,
            passwd=passwd)
        
        if originPassword is None:
            loginFailed = jsonify({
                "failed": [
                    "location": "body",
                    "userID": userID,
                    "error": "NoUser",
                    "msg": "user not found!"
                ]
            })
            return loginFailed, 404
        
        uuidTuple = dbconn.Database.getUUID(
            userID=userID, passwd=passwd)

        if originPassword[1] == password:
             loginSuccessed = jsonify({
                "userID": userID,
                "UUID": uuidTuple[2]
            })
            return loginSuccessed, 200
        else
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
@app.route("/customer/<UUID>", method=['POST'])
def customerList():
    

if __name__ == "__main__":