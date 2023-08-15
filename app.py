from movie_web_app_sqlite.api_handling.api import api
from flask import Flask, render_template, request, redirect, url_for, flash
from movie_web_app_sqlite.data_managing.sqlite_data_manager import SQLiteDataManager
from movie_web_app_sqlite.data_managing.database import db
from movie_web_app_sqlite.data_managing.data_models import User, Movie, Review
import os
import requests

API_URL = "http://www.omdbapi.com/"
API_KEY = "80a1549e"

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/movies.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SECRET_KEY'] = 'hardcodedyo'
app.register_blueprint(api, url_prefix='/api')
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
def list_users():
    data_manager = SQLiteDataManager(db.session)
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    data_manager = SQLiteDataManager(db.session)
    movies = data_manager.list_user_movies(user_id)
    user = User.query.get(user_id)
    return render_template('user_movies.html', movies=movies, user=user)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            user = User(name=username)
            data_manager = SQLiteDataManager(db.session)
            data_manager.add_user(user)
            flash('User added successfully!', 'success')
            return redirect(url_for('list_users'))
        else:
            flash('Username cannot be empty!', 'danger')
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_title = request.form.get('movie_title')
        if movie_title:
            response = requests.get(API_URL, params={
                'apikey': API_KEY,
                't': movie_title
            })
            data = response.json()
            if data['Response'] == 'True':
                movie = Movie(title=data['Title'], year=data['Year'], imdb_rating=float(data['imdbRating']),
                              poster_url=data['Poster'], user_id=user_id)
                data_manager = SQLiteDataManager(db.session)
                data_manager.add_movie(movie)
                flash('Movie added successfully!', 'success')
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                flash('Movie not found in the database!', 'danger')
                return redirect(url_for('add_movie', user_id=user_id))
        else:
            flash('Movie title cannot be empty!', 'danger')
            return redirect(url_for('add_movie', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    data_manager = SQLiteDataManager(db.session)
    movie = Movie.query.get(movie_id)
    if not movie:
        flash('Movie not found!', 'danger')
        return redirect(url_for('user_movies', user_id=user_id))

    if request.method == 'POST':
        new_rating = request.form.get('new_rating')
        try:
            float_rating = float(new_rating)
            movie.imdb_rating = float_rating
            data_manager.update_movie(movie)
            flash('Movie rating updated successfully!', 'success')
            return redirect(url_for('user_movies', user_id=user_id))
        except ValueError:
            flash('Invalid rating. Please enter a valid number!', 'danger')

    return render_template('update_movie.html', movie=movie, user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager = SQLiteDataManager(db.session)
    movie = Movie.query.get(movie_id)
    if not movie:
        flash('Movie not found!', 'danger')
        return redirect(url_for('user_movies', user_id=user_id))

    data_manager.delete_movie(movie_id)
    flash('Movie deleted successfully!', 'success')

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    data_manager = SQLiteDataManager(db.session)
    user = User.query.get(user_id)
    if user:
        for movie in user.movies:
            data_manager.delete_movie(movie.id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    else:
        flash('User not found!', 'danger')
    return redirect(url_for('list_users'))


@app.route('/users/<int:user_id>/add_review/<int:movie_id>', methods=['GET', 'POST'])
def add_review(user_id, movie_id):
    if request.method == 'POST':
        content = request.form.get('review_content')
        if content:
            review = Review(content=content, movie_id=movie_id)
            data_manager = SQLiteDataManager(db.session)
            data_manager.add_review(review)
            flash('Review added successfully!', 'success')
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            flash('Review cannot be empty!', 'danger')
    return render_template('add_review.html', user_id=user_id, movie_id=movie_id)


@app.route('/users/<int:user_id>/update_review/<int:review_id>', methods=['GET', 'POST'])
def update_review(user_id, review_id):
    data_manager = SQLiteDataManager(db.session)
    review = Review.query.get(review_id)

    if not review:
        flash('Review not found!', 'danger')
        return redirect(url_for('user_movies', user_id=user_id))

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            review.content = content
            data_manager.update_review(review)
            flash('Review updated successfully!', 'success')
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            flash('Content cannot be empty!', 'danger')
            return render_template('update_review.html', review=review, user_id=user_id)

    return render_template('update_review.html', review=review, user_id=user_id)


@app.route('/users/<int:user_id>/delete_review/<int:review_id>', methods=['POST'])
def delete_review(user_id, review_id):
    data_manager = SQLiteDataManager(db.session)
    review = Review.query.get(review_id)
    if review:
        data_manager.delete_review(review_id)
        flash('Review deleted successfully!', 'success')
    else:
        flash('Review not found!', 'danger')
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    app.logger.error(f"Server error: {error}")
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
