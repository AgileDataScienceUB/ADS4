# -*- coding: utf-8 -*-

# imports
import json
import logging
import os
from flask_ini import FlaskIni
from json import dumps
from flask import Flask, request, abort, jsonify, make_response
from utils import upload_file, upload_object, download_object, object_exists
import pandoras_box

# Flask init
application = Flask(__name__)
application.logger.info("application.py init")


with application.app_context():
    application.iniconfig = FlaskIni()
    application.iniconfig.read(os.environ['APP_SETTINGS'])
    application.logger.info("Loading application settings")


@application.route('/create-predictor', methods=['POST'])
def create_predictor():
    # The 'target' key and the csv file are mandatory:
    # if they're missing you have a 'bad request' error
    target = request.form.get("target")
    file = request.files.get("file")
    if target is None or file is None:
        abort(400)
    # Save the training dataset
    filename = 'data_train.csv'
    upload_file(file, filename)
    # Train the model
    selected_feats, woe_dicts, clf, scaler, valid_metrics = pandoras_box.create_predictor(
        filename,
        target,
        request.form.get("employee_id"),
        request.form.get("record_id"),
        request.form.get("hire_date"),
        request.form.get("record_date"),
        request.form.get("termination_date"),
        request.form.get("length_of_service"),
        request.form.get("age"),
        request.form.get("birth_date"),
        request.form.get("birth_year"),
        request.form.getlist("other_target_fields"),
        request.form.get("job_title")
        #request.form.get("special_field_types")
    )
    # Save the trained model for future use
    upload_object(selected_feats, "selected_feats.obj")
    upload_object(woe_dicts, "woe_dicts.obj")
    upload_object(clf, "clf.obj")
    upload_object(scaler, "scaler.obj")
    upload_object(valid_metrics, "valid_metrics.obj")
    return 'Done'

@application.route('/predict', methods=["POST"])
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
    upload_file(file, filename)
    # Download the trained model
    selected_feats = download_object("selected_feats.obj")
    woe_dicts = download_object("woe_dicts.obj")
    clf = download_object("clf.obj")
    scaler = download_object("scaler.obj")
    valid_metrics = download_object("valid_metrics.obj")
    # Get the predictions
    score, y_hat, df = pandoras_box.get_prediction(
        filename,
        selected_feats,
        woe_dicts,
        clf,
        scaler,
        request.form.get("employee_id"),
        request.form.get("record_id"),
        request.form.get("hire_date"),
        request.form.get("record_date"),
        request.form.get("termination_date"),
        request.form.get("length_of_service"),
        request.form.get("age"),
        request.form.get("birth_date"),
        request.form.get("birth_year"),
        request.form.getlist("other_target_fields"),
        request.form.get("job_title")
        #request.form.get("special_field_types")
    )
    return jsonify(y_hat.tolist())




if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0', port=3031)
