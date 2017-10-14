from flask import render_template, jsonify, request
from app import app

from ClubEngine import clubsPython3
import tweepy

import re

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
        # try:
        #     username = request.form['username']
        #     clubs = clubsPython3.returnResults(username)
        #     return jsonify({'clubs' : clubs})
        # except tweepy.TweepError as e:
        #     message = str(e)
        #     code = ""
        #     for letter in message:
        #         if letter.isdigit():
        #             code = code + letter
        #     return jsonify({'error' : message, 'code' : code})
        return request.args["twitterUsername"] + " is a valid twitter handle"
    else:
        raise InvalidUsage("Invalid twitter username", 400)

# @app.route('/process', methods=['POST'])
# def process():
#     try:
#         username = request.form['username']
#         clubs = clubsPython3.returnResults(username)
#         return jsonify({'clubs' : clubs})
#     except tweepy.TweepError as e:
#         message = str(e)
#         code = ""
#         for letter in message:
#             if letter.isdigit():
#                 code = code + letter
#         return jsonify({'error' : message, 'code' : code})
