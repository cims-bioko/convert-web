from flask import Flask

app = Flask(__name__)

from .web_api import convert_api

app.register_blueprint(convert_api)

