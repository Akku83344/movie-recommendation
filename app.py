import pickle
import bz2file as bz2
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import gunicorn

app = Flask(__name__)
CORS(app)

def decompress_pickle(file):
    data = bz2.BZ2File(file, "rb")
    data = pickle.load(data)
    return data

movies_model = decompress_pickle("movie/movie_list.pbz2")
similarity_model = decompress_pickle("movie/similarity.pbz2")


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


@app.route('/api/movie_list', methods=['GET'])
def get_movie_list():
    movies = movies_model
    movie_list = movies['title'].values.tolist()
    return jsonify({'movie_list': movie_list})

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    selected_movie = data.get('selected_movie')
    movies = movies_model  # Load movies
    similarity = similarity_model  # Load similarity matrix
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
    return jsonify({
        'recommended_movie_names': recommended_movie_names,
        'recommended_movie_posters': recommended_movie_posters
    })

if __name__ == '__main__':
    app.run(debug=True)
