from flask import Flask, flash, render_template, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename
# from werkzeug.exceptions import RequestEntityTooLarge
import os
import json
from benford_test import benford_test

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/khaili/benford_flaskapp/uploads'
app.config["ALLOWED_FILE_EXTENSIONS"] = ["TSV"]
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 #jaka wielkosc pliku
app.secret_key = 'psdfuhspdfh1341234' #co to jest

@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename): #przykladowy plik jest bez rozszerzenia
    if "." in filename:
        ext = filename.rsplit(".", 1)[1]
        if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return True
        else:
            return False
    else:
        return True


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        if 'tsv_file' not in request.files:
            flash('No file part')
            return redirect('/')#url_for(index)
        tsv_file = request.files["tsv_file"]
        if tsv_file.filename == '':#nie do konca rozumiem czemu w dokumentacji flaska to jest sprawdzane po poprzednim if
            flash('No selected file')
            return redirect('/')
        if tsv_file and allowed_file(tsv_file.filename):
            filename = secure_filename(tsv_file.filename)
            fpath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            tsv_file.save(fpath)
            differ = benford_test(fpath)
            # except RequestEntityTooLarge:
                #zrobic test z za duzym
                # flash('The file is bigger than allowed: {}b'.format(app.config['MAX_CONTENT_LENGTH']))
            #dlaczego nie zrobic tego except IsADirectoryError:
            #try save w wypadku niepowodzenia zapisania zwroc komunikat
            # return redirect(url_for('plot'))
            return render_template('/plot.html', url='/static/images/plot.png', differ=differ)
            # return redirect(url_for('plot'), differ=differ)
        #jakis blad jak nie znajdzie obrazka czy cos
    return redirect('/')

# @app.route('/plot/<differ>')
# @app.route('/plot')
# def plot():
#     return render_template('plot.html', url='/static/images/plot.png')
    # def plot(differ):
    # return render_template('plot.html', url='/static/images/plot.png', differ=differ)

if __name__ == '__main__':
    app.run(debug=True)
