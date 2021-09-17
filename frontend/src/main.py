import os

from flask import Flask
from flask.templating import render_template
app = Flask(__name__)
app.secret_key = os.urandom(20)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
