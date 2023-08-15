from movie_web_app_sqlite.data_managing.data_manager_interface import DataManagerInterface
from movie_web_app_sqlite.data_managing.data_models import User, Movie, Review


class SQLiteDataManager(DataManagerInterface):

    def __init__(self, db_session):
        self.session = db_session

    def list_all_users(self):
        return User.query.all()

    def list_user_movies(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.movies
        return []

    def add_user(self, user):
        self.session.add(user)
        self.session.commit()

    def add_movie(self, movie):
        self.session.add(movie)
        self.session.commit()

    def update_movie(self, movie):
        current_movie = Movie.query.get(movie.id)
        if current_movie:
            current_movie.title = movie.title
            current_movie.year = movie.year
            current_movie.imdb_rating = movie.imdb_rating
            current_movie.user_id = movie.user_id
            self.session.commit()

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            self.session.delete(movie)
            self.session.commit()

    def add_review(self, review):
        self.session.add(review)
        self.session.commit()

    def update_review(self, review):
        current_review = Review.query.get(review.id)
        if current_review:
            current_review.content = review.content
            self.session.commit()

    def delete_review(self, review_id):
        review = Review.query.get(review_id)
        if review:
            self.session.delete(review)
            self.session.commit()
