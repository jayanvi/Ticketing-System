from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"status": "app is running"})


@app.route("/tickets")
def get_tickets():
    return jsonify({"status": "endpoint works"})
