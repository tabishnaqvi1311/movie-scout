import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similMatrix.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)
api_key = st.secrets["api_keys"]["tmdb"]

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended, posters = [], []
    for i in movie_list:
        title, id = movies.iloc[i[0]].title, movies.iloc[i[0]].movie_id
        recommended.append(title)
        posters.append(fetch_poster(id))
    return recommended, posters


st.title("Movie Scout")

selected_name = option = st.selectbox(
    "Pick a movie to watch :)", movies['title'].values
)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])

