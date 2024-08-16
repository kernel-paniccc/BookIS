from flask import flash, render_template, request, redirect

from flask_login import login_user, login_required, logout_user, current_user

from app.database.models import User
from Flask_app.init import app
from app.database.models import async_session
from sqlalchemy import select

import os


@app.route('/', methods=['GET', 'POST'])
async def login():
    try:
        tg_id = request.form.get('id')
        password = request.form.get('password')
        async with async_session() as session:
            result = await session.execute(select(User).where(User.tg_id == tg_id))
            user = result.scalars().first()
            if user is not None and str(user.password) == str(password):
                login_user(user)
                return redirect("/mkgtjtbjnj")
            else:
                flash("некорректные данные", category='error')
    except Exception as e:
        print(e)
        flash(str(e), category='error')

    return render_template('login_page.html')

