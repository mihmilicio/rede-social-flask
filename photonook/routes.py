# Aqui vai as rotas e links

from flask import render_template, redirect, url_for
from flask_login import login_user

from photonook.models import User
from photonook import app, database
from photonook.forms import FormLogin, FormRegister
from photonook import bcrypt


@app.route('/register', methods=['POST', 'GET'])
def register():
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

@app.route('/login', methods=['POST', 'GET'])
def login():
    formLogin = FormLogin()

    if formLogin.validate_on_submit():
        userToLogin = User.query.filter_by(email=formLogin.email.data).first()
        if userToLogin and bcrypt.check_password_hash(userToLogin.password, formLogin.password.data):
            login_user(userToLogin)
            return redirect(url_for('home'))


    return render_template("login.html", form=formLogin)