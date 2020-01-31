from flask import Flask
from app.controllers.core import setup

setup()
app = Flask(__name__)

from app import routes