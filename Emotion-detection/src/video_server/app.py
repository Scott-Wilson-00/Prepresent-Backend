from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_cors import CORS
from src.emotions import process_sentiment, calculate_emotions


app = Flask(__name__)
CORS(app)

presenting = False
emotions = None

@app.route('/')
def index():
    global presenting
    
    if emotions:
        context = { "presenting": presenting, 
                    "emotions": emotions,
                    "angry": emotions["Angry"],
                    "disgusted": emotions["Disgusted"],
                    "fearful": emotions["Fearful"],
                    "happy": emotions["Happy"],
                    "neutral": emotions["Neutral"],
                    "sad": emotions["Sad"],
                    "surprised": emotions["Surprised"],
                    }
    else:

        context = { "presenting": presenting, "emotions": emotions }
    return render_template('index.html', **context)

@app.route('/', methods=['POST'])
def upload_file():
    fileName = request.files['file']
    if fileName.filename != '':
        fileName.save(fileName.filename)
    return redirect(url_for('index'))

@app.route('/present')
def present():
    global presenting
    presenting = True
    global emotions
    emotions = None
    # GET request
    if request.method == 'GET':
        response = Response(process_sentiment(), mimetype='multipart/x-mixed-replace;boundary=frame')# serialize and use JSON headers
        return response

@app.route('/stop-presenting')
def stop_presenting():
    global presenting
    presenting = False

    if request.method == "GET":
        global emotions
        emotions = calculate_emotions()
        return {}

app.run(debug = True, port = 8080)