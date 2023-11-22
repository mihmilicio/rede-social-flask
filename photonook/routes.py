import os

from flask import render_template, redirect, url_for, session, request, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, date

from photonook.models import User, Post, PostLike
from photonook import app, database
from photonook.forms import FormLogin, FormRegister, FormCreateNewPost
from photonook import bcrypt

@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for('login'))

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/", methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
  _formNewPost = FormCreateNewPost()
  _basedir = os.path.abspath(os.path.dirname(__file__))

  if _formNewPost.validate_on_submit():
    _post_text = _formNewPost.text.data

    _post_img = _formNewPost.photo.data
    _img_name = secure_filename(_post_img.filename)
    _final_path = os.path.join(_basedir, app.config['UPLOAD_FOLDER'], _img_name)

    _post_img.save(_final_path)

    newPost = Post(post_text=_post_text,
                    post_img=_img_name,
                    user_id=int(current_user.id)
                    )

    database.session.add(newPost)
    database.session.commit()

    return redirect(url_for('home'))

  users = User.query.all()
  users.remove(current_user)
  users.insert(0, current_user)

  posts = Post.query.all()
  posts.sort(key=lambda post: datetime.strptime(post.creation_date, '%Y-%m-%d %H:%M:%S.%f'), reverse=True)
  new_posts = []

  for post in posts:
    new_post = post
    new_post.post_img = os.path.join(app.config['UPLOAD_FOLDER'], post.post_img).replace("\\","/")
    new_post.creation_date = datetime.strptime(post.creation_date, '%Y-%m-%d %H:%M:%S.%f').strftime("%d/%m/%Y at %H:%M")
    new_post.user = User.query.get(int(post.user_id))
    new_post.liked = bool(PostLike.query.get((current_user.id, post.id)))
    new_post.like_count = len(post.likes)
    new_posts.append(new_post)

  return render_template("home.html", users=users, user=None, form=_formNewPost, posts=new_posts)


@app.route('/profile/<user_id>', methods=['POST', 'GET'])
@login_required
def profile(user_id):
  _formNewPost = FormCreateNewPost()
  _basedir = os.path.abspath(os.path.dirname(__file__))

  if _formNewPost.validate_on_submit():
      _post_text = _formNewPost.text.data

      _post_img = _formNewPost.photo.data
      _img_name = secure_filename(_post_img.filename)
      _final_path = os.path.join(_basedir, app.config['UPLOAD_FOLDER'], _img_name)

      _post_img.save(_final_path)

      newPost = Post(post_text=_post_text,
                      post_img=_img_name,
                      user_id=int(current_user.id)
                      )

      database.session.add(newPost)
      database.session.commit()

      return redirect(url_for('profile', user_id))

  _user = User.query.get(int(user_id))

  users = User.query.all()
  users.remove(current_user)
  users.insert(0, current_user)

  posts = _user.posts
  posts.sort(key=lambda post: datetime.strptime(post.creation_date, '%Y-%m-%d %H:%M:%S.%f'), reverse=True)
  new_posts = []

  for post in posts:
    new_post = post
    new_post.post_img = os.path.join(app.config['UPLOAD_FOLDER'], post.post_img).replace("\\","/")
    new_post.creation_date = datetime.strptime(post.creation_date, '%Y-%m-%d %H:%M:%S.%f').strftime("%d/%m/%Y at %H:%M")
    new_post.user = User.query.get(int(post.user_id))
    new_post.liked = bool(PostLike.query.get((current_user.id, post.id)))
    new_post.like_count = len(post.likes)
    new_posts.append(new_post)
  
  if int(user_id) == int(current_user.id):
    return render_template("home.html", users=users, user=_user, form=_formNewPost, posts=posts)
  
  return render_template("home.html", users=users, user=_user, form=None, posts=_user.posts)

@app.route('/like/<post_id>', methods=['PATCH'])
@login_required
def like(post_id):
  post = Post.query.get(post_id)
  liked = PostLike.query.get((current_user.id, post_id))

  if liked:
    PostLike.query.delete
    database.session.delete(liked)
  else:
    postLike = PostLike(post_id=post_id, user_id=current_user.id)
    database.session.add(postLike)
    
  database.session.commit()

  return jsonify({"likes": len(post.likes), "liked": bool(not liked)})
