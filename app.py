import flask
from flask import Flask, request, redirect, render_template
from flask_cors import CORS, cross_origin

import spacy
from textblob import TextBlob
from gensim.summarization import summarize

from transformers import PegasusTokenizer, PegasusForConditionalGeneration, TFPegasusForConditionalGeneration
# Let's load the model and the tokenizer
model_name = "human-centered-summarization/financial-summarization-pegasus"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)


app = Flask(__name__)

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
