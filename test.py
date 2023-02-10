import os
import datetime
import logging
import sys

from dotenv import load_dotenv

load_dotenv()

from flask import Flask


ct = datetime.datetime.now()

if os.getenv("LOG_TO_FILE"):
    logging.basicConfig(filename=f"logs/{ct}.log".replace(":","-"), level=logging.DEBUG)
    """
    logger = logging.getLogger()
    sys.stderr.write = logger.error
    sys.stdout.write = logger.info
    """

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
