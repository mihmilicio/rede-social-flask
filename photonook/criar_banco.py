from photonook import database, app
from photonook.models import User, Post

with app.app_context():
    database.create_all()
