from flask import render_template, jsonify, request
from app import app

from ClubEngine import clubsPython3
import tweepy

import re
import json

"""
HTTP ERROR HANDLER
"""
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/api/recommend', methods=['GET'])
def clubReccomendation():
    # Check that the twitterUsername is valid with regex
    if re.fullmatch("^@?[a-zA-Z_0-9]{1,15}", request.args["twitterUsername"]):
        try:
            username = request.args["twitterUsername"]
            clubs = clubsPython3.returnResults(username)
            return jsonify(clubs)
        except tweepy.TweepError as e:
            raise InvalidUsage(e.response.json()["errors"][0]["message"], e.response.status_code)
    else:
        raise InvalidUsage("Invalid twitter username", 400)