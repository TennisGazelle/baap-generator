from flask import Flask, request, send_file
from validator import generateRelease

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = "."

PORT=5000

@app.route("/", methods=["GET"])
def home():
    return "<h1>Hi there!!!</h1>"

@app.route("/generate", methods=["POST"])
def generate():
    generateRelease()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
