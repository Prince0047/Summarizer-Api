import flask
from flask import Flask, request, redirect, render_template, send_file, send_from_directory, session
from flask_cors import CORS, cross_origin

import os
# import glob
from werkzeug.utils import secure_filename

import spacy
from textblob import TextBlob
from gensim.summarization import summarize

# from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration
# # Let's load the model and the tokenizer
# model_name = "human-centered-summarization/financial-summarization-pegasus"
# tokenizer = PegasusTokenizer.from_pretrained(model_name)
# model = PegasusForConditionalGeneration.from_pretrained(model_name)

UPLOAD_FOLDER = 'uploads/'
UPLOAD_FOLDER2 = 'uploads2/'
#app = Flask(__name__)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 30

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

CORS(app)


@app.route('/')
def main():
    return render_template("index.htm")


@app.route('/sum', methods=["GET", "POST"])
def Sum():
    if request.method == "OPTIONS":  # CORS preflight
        return build_cors_preflight_response()
    elif request.method == "POST":  # The actual request following the preflight
        file_uploaded = request.get_json()
        data_up = file_uploaded['data']
        percent = int(file_uploaded['perc'])

        percent = percent/100
        summary_result = summarize(data_up, percent)
        response = {
            'headers': ["*", "Access-Control-Allow-Origin"],
            'status': 200,
            'data': summary_result
        }
    return response


@app.route('/model')
def abs_model():
    return render_template("working.htm")




# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Removing Files
        # Pfiles = glob.glob('uploads/*')
        # for f in Pfiles:
        #     os.remove(f)

        # Pfiles2 = glob.glob('uploads2/*')
        # for f in Pfiles2:
        #     os.remove(f)
        req = request.form
        # check if the post request has the file part
        if req['form-name'] == 'form1':
            text_area = req['txtarea']
            percent = int(req['percent'])
            percent = percent/100
            print(percent)
            sum_text = summarize(text_area, percent)
            return render_template('upload_file.html', in_text=text_area, sum_text=sum_text)
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            text = " ".join((line for line in open(os.path.join(app.config['UPLOAD_FOLDER'], filename), encoding='utf-8')))
            # os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            percent = int(req['percent'])
            percent = percent/100
            print(text)
            text2 = summarize(text, percent)
            print("after summary.....")

            # file_path = app.config['UPLOAD_FOLDER2'] 
            print(filename)
            # filename= "SUM_" + filename
            # files = open(file_path+ sum_file, 'w')
            # files.write(text2)
            # files.close()
            with open(os.path.join(app.config['UPLOAD_FOLDER2'], filename), 'w') as f:
                f.write(text2)
            print("here is the filename : ",filename)

            print("saved file successfully")
      #send file name as parameter to downlad
            # file_path = os.path.join(app.config['UPLOAD_FOLDER2'], filename)
            # print("file for sent is ::: ")
            # return send_file(file_path, as_attachment=True, attachment_filename='')
            # file_path = os.path.join(app.config['UPLOAD_FOLDER2'], filename)

            return redirect('/downloadfile/'+ filename)
    return render_template('upload_file.html', in_text="Text area for input ...")
# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)
@app.route('/return-files/<filename>')
def return_files_tut(filename):
    print("file for sent is ::: ")
    return send_from_directory(app.config['UPLOAD_FOLDER2'], filename=filename, as_attachment=True, attachment_filename="Sum_"+filename, cache_timeout=-1)


@app.route("/delete" , methods = ['GET','POST'])
def delete_Uploads():
    if request.method == 'POST':
        req = request.form
        if req['username'] == "Prince0047" and req['password'] == "qwerty0047":

            # files = glob.glob('uploads/*')
            # for f in files:
            #     os.remove(f)

            # files2 = glob.glob('uploads2/*')
            # for f in files2:
            #     os.remove(f)
            
            
            return "Data files have been deleted..."
        
        else:
            return "Wrong Id or password"
    

    return render_template('delete.html')


# Preflight Response


def build_cors_preflight_response():
    response = flask.make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Controll-Allow-Headers", "*")
    response.headers.add("Access-Controll-Allow-Methods", "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(debug=True)
