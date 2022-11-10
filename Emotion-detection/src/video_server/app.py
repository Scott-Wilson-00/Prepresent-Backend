from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    fileName = request.files['file']
    if fileName.filename != '':
        fileName.save(fileName.filename)
    return redirect(url_for('index'))