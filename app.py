from flask import Flask,render_template, flash, request, redirect, url_for,send_from_directory
from werkzeug.utils import secure_filename
import os
import imageAI_predictor_image

UPLOAD_FOLDER = './templates/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename): #Проверка расширение
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # Если пользователь не выбрал файл, то браузер отправляет пустой файл без имени.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('analysis', name=filename))
            #return redirect(url_for('download_file', name=filename))
    return render_template('upload.html')

@app.route('/analysis/<name>')
def analysis(name):
    text=imageAI_predictor_image.start(app.config['UPLOAD_FOLDER'],name)
    img="/uploads/"+name
    return render_template('analysis.html', name=name, ret=text,file=img)

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html', title='Отбор')
