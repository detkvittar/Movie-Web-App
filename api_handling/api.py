from flask import Blueprint, jsonify, request
from movie_web_app_sqlite.data_managing.data_models import User, Movie
import requests
from movie_web_app_sqlite.data_managing.database import db

api = Blueprint('api', __name__)

API_URL = "http://www.omdbapi.com/"
API_KEY = "80a1549e"


@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.name for user in users])


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    movies = [movie.title for movie in user.movies]
    return jsonify(movies)


@api.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    movie_title = request.json.get('movie_title')
    if not movie_title:
        return jsonify({'error': 'Movie title is required'}), 400

    response = requests.get(API_URL, params={
        'apikey': API_KEY,
        't': movie_title
    })
    data = response.json()

    if data['Response'] == 'True':
        movie = Movie(
            title=data['Title'],
            year=data['Year'],
            imdb_rating=float(data['imdbRating']),
            poster_url=data['Poster'],
            user_id=user_id
        )
        db.session.add(movie)
        db.session.commit()
        return jsonify({'message': 'Movie added successfully', 'movie': data['Title']}), 201
    else:
        return jsonify({'error': 'Movie not found in the database'}), 404
