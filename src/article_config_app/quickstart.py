import json

from flask import Flask, request, jsonify
import sqlite3
import os

# Init app
app = Flask(__name__)


# Flask maps HTTP requests to Python functions.
# The process of mapping URLs to functions is called routing.
@app.route('/', methods=['GET'])
def home():
    return "<p>This is a prototype API</p>"


# A route to return all of available entries i our catalog.
@app.route('/hello', methods=['GET'])
def api_all():
    response = {
        "dear": "user",
        "hello": "world"
    }
    return json.dumps(response), 200
    # return jsonify(all_books)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found</p>", 404


# A method that runs the application server.
if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=False, threaded=True, port=5000)