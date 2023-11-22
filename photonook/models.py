from photonook import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.relationship("Post", backref='user', lazy=True)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    post_text = database.Column(database.String, default='')
    post_img = database.Column(database.String, default='default.png')
    creation_date = database.Column(database.String, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    likes = database.relationship('PostLike', backref='post', passive_deletes=True)

class PostLike(database.Model):
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False, primary_key=True)
    post_id = database.Column(database.Integer, database.ForeignKey('post.id'), nullable=False, primary_key=True)
