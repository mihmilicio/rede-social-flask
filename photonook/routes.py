# Aqui vai as rotas e links

from flask import render_template, redirect, url_for
from flask_login import login_user

from photonook.models import User
from photonook import app, database
from photonook.forms import FormRegister
from photonook import bcrypt


@app.route('/register', methods=['POST', 'GET'])
def create_account():
    formRegister = FormRegister()

    if formRegister.validate_on_submit():
        password = formRegister.password.data
        password_cr = bcrypt.generate_password_hash(password)

        newUser = User(username=formRegister.username.data,
                       email=formRegister.email.data,
                       password=password_cr)

        database.session.add(newUser)
        database.session.commit()
        login_user(newUser, remember=True)
        return redirect(url_for('home'))

    return render_template("register.html", form=formRegister)
