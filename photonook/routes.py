import os

from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from photonook.models import User, Post
from photonook import app, database
from photonook.forms import FormLogin, FormRegister, FormCreateNewPost
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


@app.route("/", methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
  _formNewPost = FormCreateNewPost()

  if _formNewPost.validate_on_submit():
    _post_text = _formNewPost.text.data
    _post_img = _formNewPost.photo.data
    _img_name = secure_filename(_post_img.filename)
    path = os.path.abspath(os.path.dirname(__file__))
    path2 = app.config['UPLOAD_FOLDER']
    _final_path = f'{path}/{path2}/{_img_name}'

    _post_img.save(_final_path)

    newPost = Post(post_text=_post_text,
                    post_img=_img_name,
                    user_id=int(current_user.id)
                    )

    # salvar no banco
    database.session.add(newPost)
    database.session.commit()

  users = User.query.all()

  return render_template("home.html", users=users, user=None, form=_formNewPost, posts=current_user.posts)


@app.route('/profile/<user_id>', methods=['POST', 'GET'])
@login_required
def profile(user_id):
  _formNewPost = FormCreateNewPost()
  if _formNewPost.validate_on_submit():
      # pegar o texto
      _post_text = _formNewPost.text.data

      # pegar a img
      _post_img = _formNewPost.photo.data
      _img_name = secure_filename(_post_img.filename)
      _basedir = os.path.abspath(os.path.dirname(__file__))
      print(_basedir)
      path2 = app.config['UPLOAD_FOLDER']
      print(path2)
      _final_path = os.path.join(_basedir, app.config['UPLOAD_FOLDER'], _img_name)
      print(_final_path)

      _post_img.save(_final_path)

      newPost = Post(post_text=_post_text,
                      post_img=_img_name,
                      user_id=int(current_user.id)
                      )

      # salvar no banco
      database.session.add(newPost)
      database.session.commit()

  _user = User.query.get(int(user_id))
  users = User.query.all()

  if int(user_id) == int(current_user.id):
    return render_template("home.html", users=users, user=_user, form=_formNewPost, posts=_user.posts)
  
  return render_template("home.html", users=users, user=_user, form=None, posts=_user.posts)