# server.py
# Author: Thomas MINIER - MIT License 2017-2018
from flask import Flask, render_template
from flask_cors import CORS
from os import environ
from database.datasets import DatasetCollection
from http_server.sparql_interface import sparql_blueprint

config_file = "data/test_config.yaml"
if 'YALDF_CONFIG' in environ:
    config_file = environ['YALDF_CONFIG']

# load datasets from config file
datasets = DatasetCollection(config_file)

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    datasets_infos = datasets._config["datasets"]
    return render_template("index_sage.html", datasets=datasets_infos)


@app.route('/clients')
def clients():
    return render_template("clients.html")


@app.route('/documentation')
def doc():
    return render_template("documentation.html")


# Register Blueprints which implement all available LDF interfaces
# For example, http_server.tpf contains the blueprint for TPF interface
app.register_blueprint(sparql_blueprint(datasets, app.logger))
