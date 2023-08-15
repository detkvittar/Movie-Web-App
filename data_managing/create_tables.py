from movie_web_app_sqlite.data_managing.database import db
from movie_web_app_sqlite.app import app

with app.app_context():
    db.create_all()