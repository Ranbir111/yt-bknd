from flask import Flask, request, jsonify
from pytube import YouTube
import re
import os
from pathlib import Path
# from flask_cors import CORS, cross_origin
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/videodetails', methods=['POST'])
@cross_origin()
def videodetails():
    if request.method == 'POST':
        data = request.get_json()
        video_url = data['url']
        try:
            yt = YouTube(video_url)
            data = {
                "title":yt.title,
                "thumbnail_url":yt.thumbnail_url
            }
            return jsonify(data)
        except Exception as e:
            return f"An error occurred: {str(e)}"


@app.route('/downloadvideo', methods=['POST'])
@cross_origin()
def downloadvideo():
    if request.method == 'POST':
        data = request.get_json()
        video_url = data['url']
        try:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            path_to_download = str(os.path.join(Path.home(), 'Videos'))
            stream.download(path_to_download)  # Save the video in the 'downloads' folder
            return jsonify({"success":"true"})
        except Exception as e:
            return f"An error occurred: {str(e)}"

@app.route('/downloadaudio', methods=['POST'])
@cross_origin()
def downloadaudio():
    if request.method == 'POST':
        data = request.get_json()
        video_url = data['url']
        try:
            yt = YouTube(video_url)
            stream = yt.streams.filter(only_audio=True)
            path_to_download = str(os.path.join(Path.home(), 'Music'))
            stream[0].download(path_to_download)  # Save the video in the 'downloads' folder
            return jsonify({"success":"true"})
        except Exception as e:
            return f"An error occurred: {str(e)}"

app.run()