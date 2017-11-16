# -*- coding: utf-8 -*-

# imports
import json
import logging
import os
from flask import Flask, jsonify, request
from flask_ini import FlaskIni
from utils import Utils

# Flask init
application = Flask(__name__)
application.logger.info("Application.py init")


with application.app_context():
    application.iniconfig = FlaskIni()
    application.iniconfig.read(os.environ['APP_SETTINGS'])
    application.logger.info("Loading APP Settings")


@application.route('/', methods=['GET'])
def hello_world():
    return "Hello World from Flask"



if __name__ == '__main__':
    application.debug = True
    application.run(host='0.0.0.0', port=4000)
