from flask import Flask

app: Flask = Flask(__name__)
from app.routes.routes import *