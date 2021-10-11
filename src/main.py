from flask import Flask, request, send_file
from validator import Validator
import logging
import json
import os
import sys
# sys.path[0] = sys.path[0][:-4] # TRYING TO GET US OUT OF SRC/

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = "."

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__doc__)

PORT=5000

v = Validator()

@app.route("/", methods=["GET"])
def home():
    return "<h1>Hi there!!!</h1>"

@app.route("/generate", methods=["POST"])
def generate():
    return v.generate_project()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
