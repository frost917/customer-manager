import os

from flask import Flask, Response, g, Blueprint
app = Flask(__name__)
app.secret_key = os.urandom(20)
