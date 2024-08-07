from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv

import os, base64

load_dotenv()

app = Flask(__name__)

app.secret_key = base64.b64encode(str(os.getenv('APP_SEC_KEY')).encode())

app.config["SQLALCHEMY_DATABASE_URI"] = str(os.getenv('URL'))

manager = LoginManager(app)

from Flask_app import routers