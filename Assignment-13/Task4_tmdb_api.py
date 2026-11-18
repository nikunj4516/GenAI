# Task 4: API Mini Project (TMDB Movie Data Collector)
# To use the live API: get a free key from themoviedb.org (Settings -> API) and set it
#   Windows: setx TMDB_API_KEY "your_key"   (then open a new terminal)
#   Mac/Linux: export TMDB_API_KEY="your_key"
import os
import requests
import pandas as pd

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


def get_movies(category, pages=5):
    # every page has 20 movies
    movies = []
    for page in range(1, pages + 1):
        response = requests.get(f"{BASE_URL}/movie/{category}",
                                params={"api_key": API_KEY, "page": page}, timeout=15)
        response.raise_for_status()
        movies += response.json()["results"]
    return movies


def get_data_from_api():
    if not API_KEY:
        raise ValueError("TMDB_API_KEY is not set")

    # genre id -> genre name
    response = requests.get(f"{BASE_URL}/genre/movie/list", params={"api_key": API_KEY}, timeout=15)
    response.raise_for_status()
    genre_map = {g["id"]: g["name"] for g in response.json()["genres"]}

    # popular movies + top rated movies (extra)
    popular = pd.DataFrame(get_movies("popular"))
    popular["source"] = "popular"
    top_rated = pd.DataFrame(get_movies("top_rated"))
    top_rated["source"] = "top_rated"

    df = pd.concat([popular, top_rated], ignore_index=True).drop_duplicates(subset="id")
    df["genres"] = df["genre_ids"].apply(lambda ids: ", ".join(genre_map.get(i, "") for i in ids))
    df = df.rename(columns={"vote_average": "rating"})
    return df[["id", "title", "release_date", "rating", "vote_count", "popularity",
               "original_language", "genres", "source"]]


def get_sample_data():
    # Reason for this sample data: when I tried to use the TMDB website / API it was not
    # available, so the live data could not be collected. To keep the task working, this
    # file creates tmdb_movies.csv from a small sample with the same columns as the API data.
    # The movies are real, but the ratings and popularity numbers are only approximate
    # sample values, not live data from TMDB.
    columns = ["id", "title", "release_date", "rating", "vote_count", "popularity",
               "original_language", "genres", "source"]
    rows = [
        (278, "The Shawshank Redemption", "1994-09-23", 8.7, 28000, 95.2, "en", "Drama, Crime", "top_rated"),
        (238, "The Godfather", "1972-03-14", 8.7, 21000, 88.4, "en", "Drama, Crime", "top_rated"),
        (240, "The Godfather Part II", "1974-12-20", 8.6, 13000, 62.1, "en", "Drama, Crime", "top_rated"),
        (424, "Schindler's List", "1993-12-15", 8.6, 16000, 55.3, "en", "Drama, History, War", "top_rated"),
        (389, "12 Angry Men", "1957-04-10", 8.5, 8000, 40.7, "en", "Drama", "top_rated"),
        (129, "Spirited Away", "2001-07-20", 8.5, 16000, 90.8, "ja", "Animation, Family, Fantasy", "top_rated"),
        (19404, "Dilwale Dulhania Le Jayenge", "1995-10-20", 8.5, 5000, 30.6, "hi", "Comedy, Drama, Romance", "top_rated"),
        (496243, "Parasite", "2019-05-30", 8.5, 18000, 85.9, "ko", "Comedy, Thriller, Drama", "top_rated"),
        (680, "Pulp Fiction", "1994-09-10", 8.5, 27000, 70.5, "en", "Thriller, Crime", "top_rated"),
        (155, "The Dark Knight", "2008-07-16", 8.5, 32000, 110.4, "en", "Drama, Action, Crime, Thriller", "top_rated"),
        (13, "Forrest Gump", "1994-06-23", 8.5, 27000, 82.3, "en", "Comedy, Drama, Romance", "top_rated"),
        (27205, "Inception", "2010-07-15", 8.4, 38000, 120.7, "en", "Action, Science Fiction, Adventure", "popular"),
        (157336, "Interstellar", "2014-11-05", 8.4, 35000, 130.2, "en", "Adventure, Drama, Science Fiction", "popular"),
        (550, "Fight Club", "1999-10-15", 8.4, 30000, 98.6, "en", "Drama, Thriller", "popular"),
        (603, "The Matrix", "1999-03-30", 8.2, 25000, 91.9, "en", "Action, Science Fiction", "popular"),
        (299534, "Avengers: Endgame", "2019-04-24", 8.2, 26000, 140.3, "en", "Adventure, Science Fiction, Action", "popular"),
        (475557, "Joker", "2019-10-01", 8.1, 24000, 105.1, "en", "Crime, Thriller, Drama", "popular"),
        (872585, "Oppenheimer", "2023-07-19", 8.1, 9000, 150.8, "en", "Drama, History", "popular"),
        (438631, "Dune", "2021-09-15", 7.8, 12000, 115.5, "en", "Science Fiction, Adventure", "popular"),
        (634649, "Spider-Man: No Way Home", "2021-12-15", 8.0, 19000, 125.9, "en", "Action, Adventure, Science Fiction", "popular"),
    ]
    return pd.DataFrame(rows, columns=columns)


try:
    df = get_data_from_api()
    print("Data collected from the TMDB API")
except (requests.exceptions.RequestException, ValueError) as error:
    print("TMDB API is not available:", error)
    print("Using the sample data instead")
    df = get_sample_data()

# save the data
df.to_csv("tmdb_movies.csv", index=False)
print("Saved tmdb_movies.csv", df.shape)
print(df[["title", "release_date", "rating", "popularity"]].head(10))