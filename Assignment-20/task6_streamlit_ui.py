"""
PART 4 - Task 6: Build UI using Streamlit

Simple interface:
  - Dropdown to select a movie
  - Button to generate recommendations
  - Recommended movies displayed clearly

Run (from the project root):  streamlit run app.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st

from task5_recommend_function import (
    get_model,
    get_titles,
    recommend,
)


@st.cache_resource(show_spinner="Loading data and building the model...")
def load_model():
    get_model()
    return True


def main():
    st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")
    load_model()

    st.title("🎬 Movie Recommendation System")
    st.write("Content-based recommendations using TF-IDF and cosine similarity.")

    movie = st.selectbox("Select a movie", get_titles())
    top_n = st.slider("Number of recommendations", min_value=3, max_value=10, value=5)

    if st.button("Recommend"):
        results = recommend(movie, top_n)
        st.subheader(f"Because you picked: {movie}")
        for i, row in results.iterrows():
            st.markdown(f"**{i + 1}. {row['title']}**")
            st.caption(
                f"Genres: {row['genres']}  |  Rating: {row['vote_average']}  |  "
                f"Similarity: {row['similarity']:.2f}"
            )
            st.write(row["overview"])
            st.divider()


if __name__ == "__main__":
    main()
