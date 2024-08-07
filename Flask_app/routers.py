from flask import jsonify

from app.database.models import User
from Flask_app.init import app
from app.database.models import async_session
from sqlalchemy import select

import os
@app.route('/', methods=['GET', 'POST'])
async def login():
    async with async_session() as session:
        stmt = select(User).order_by(User.id)
        result = await session.execute(stmt)
        user_list = result.scalars().all()
    return jsonify([{'id': user.id, 'tg_id': user.tg_id, 'password': user.password} for user in reversed(user_list)])
