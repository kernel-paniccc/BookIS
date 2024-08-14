from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from app.database.models import User, async_session
from sqlalchemy import select

import os, base64

load_dotenv()

app = Flask(__name__)

app.secret_key = base64.b64encode(str(os.getenv('APP_SEC_KEY')).encode())

app.config["SQLALCHEMY_DATABASE_URI"] = str(os.getenv('URL'))


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
async def load_user(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

from Flask_app import routers