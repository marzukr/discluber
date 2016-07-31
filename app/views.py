from flask import Flask, render_template, jsonify, request
from app import app

import clubsPython3
import tweepy

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/process', methods=['POST'])
def process():
    try:
        username = request.form['username']
        clubs = clubsPython3.returnResults(username)
        return jsonify({'clubs' : clubs})
    except tweepy.TweepError as e:
        message = str(e)
        code = ""
        for letter in message:
            if letter.isdigit():
                code = code + letter
        return jsonify({'error' : message, 'code' : code})
