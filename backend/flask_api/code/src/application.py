# -*- coding: utf-8 -*-

# imports
import json
import logging
import os
from flask_ini import FlaskIni
from json import dumps
from flask import Flask, request, abort, jsonify, make_response, redirect, flash, url_for
from utils import upload_file, upload_object, download_object, object_exists
from werkzeug.utils import secure_filename
import pandoras_box
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = '/data'
ALLOWED_EXTENSIONS = ['csv']

# Flask init
application = Flask(__name__)
application.logger.info("application.py init")
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


with application.app_context():
    application.iniconfig = FlaskIni()
    application.iniconfig.read(os.environ['APP_SETTINGS'])
    application.logger.info("Loading application settings")

CORS(application)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@application.route('/create-predictor', methods=['POST'])
@cross_origin()
def create_predictor():
    # Collecting fields. Target and file are mandatories
    target = request.form.get("target")
    file = request.files.get("file")
    employee_id = request.form.get("employee_id")
    length_of_service = request.form.get("length_of_service")
    age = request.form.get("age")
    job_title = request.form.get("job_title")

    if target is None or file is None:
        abort(400)
    # Save the training dataset
    filename = 'data_train.csv'
    upload_file(file, filename)

    # Train the model
    selected_feats,woe_dicts,clf,scaler,valid_metrics,dict_A5 = pandoras_box.create_predictor(
        filename,
        target,
        employee_id=employee_id,
        length_of_service=length_of_service,
        age=age,
        job_title=job_title)

    # Save the trained model for future use
    upload_object(selected_feats, "selected_feats.obj")
    upload_object(woe_dicts, "woe_dicts.obj")
    upload_object(clf, "clf.obj")
    upload_object(scaler, "scaler.obj")
    upload_object(valid_metrics, "valid_metrics.obj")

    # Response body
    response = jsonify({'Result': 'Model successfully trained'})

    # Managing response CORS
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
    response.headers.add('Access-Control-Max-Age', '5000')
    response.headers.add('Access-Control-Allow-Headers', 'x-requested-with, Content-Type, Accept-Encoding, Accept-Language, Cookie, Referer')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@application.route('/predict', methods=["POST", 'OPTIONS'])
@cross_origin()
def predict():
    # The csv file is mandatory:
    # if it's missing you have a 'bad request' error

    file = request.files.get("file")
    if file is None:
        abort(400)

    # It is mandatory to have a trained model
    # Without that, you have a 'bad request' error
    if  object_exists("selected_feats.obj") is False \
        or object_exists("woe_dicts.obj") is False \
        or object_exists("clf.obj") is False \
        or object_exists("scaler.obj") is False \
        or object_exists("valid_metrics.obj") is False:
        abort(400)
    # Save the test dataset

    filename = 'data_test.csv'
    employee_id = request.form.get("employee_id")
    length_of_service = request.form.get("length_of_service")
    age = request.form.get("age")
    job_title = request.form.get("job_title")


    filename = 'data_test.csv'
    upload_file(file, filename)

    # Download the trained model
    selected_feats = download_object("selected_feats.obj")
    woe_dicts = download_object("woe_dicts.obj")
    clf = download_object("clf.obj")
    scaler = download_object("scaler.obj")
    valid_metrics = download_object("valid_metrics.obj")

    # Get the predictions
    score, y_hat = pandoras_box.get_prediction(
        filename,
        selected_feats,
        woe_dicts,
        clf,
        scaler,
        employee_id=employee_id,
        length_of_service=length_of_service,
        age=age,
        job_title=job_title)

    # Save predictions
    upload_object(score, "predict_score.obj")

    response = jsonify({'Result': 'Model successfully predicted'})
    response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
    response.headers.add('Access-Control-Max-Age', '5000')
    response.headers.add('Access-Control-Allow-Headers', 'x-requested-with, Content-Type, Accept-Encoding, Accept-Language, Cookie, Referer')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0', port=3031)
