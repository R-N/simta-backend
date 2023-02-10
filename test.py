import os
import datetime
import sys

from dotenv import load_dotenv

load_dotenv()

from flask import Flask

err = None

app = Flask(__name__)

@app.route("/")
def hello():
    return f"<h1 style='color:blue'>Hello There! {err}</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
