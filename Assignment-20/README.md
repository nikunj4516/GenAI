# 🎬 Movie Recommendation System (Content-Based)

An end-to-end content-based recommender built with **Python, Pandas, scikit-learn and Streamlit**.
Select a movie and the app returns the most similar movies using **TF-IDF** and **cosine similarity**.

- **Deployed app:** `https://<your-app-name>.onrender.com` *(replace after deploying)*
- **GitHub repo:** `https://github.com/<your-username>/movie-recommender` *(replace)*

## Dataset

| Item | Detail |
|------|--------|
| Name | TMDB 5000 Movie Dataset |
| Kaggle link | https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata |
| File used | `Movie_recommendation.csv` (4,803 rows × 20 columns) |
| Item identifier | `title` |
| Text features | `overview`, `tagline`, `genres`, `keywords` |

## Project structure

```
GenAI_Task(20)Nikunj/
├── PART1_Data_Preprocessing/
│   ├── task1_load_dataset.py
│   └── task2_text_preprocessing.py
├── PART2_Text_Vectorization/
│   ├── task3_tfidf.py
│   └── task4_cosine_similarity.py
├── PART3_Recommendation_Logic/
│   └── task5_recommend_function.py
├── PART4_Simple_App_Interface/
│   └── task6_streamlit_ui.py
├── PART5_Git_and_GitHub/
│   └── task7_git_github_setup.md
├── PART6_Deployment_on_Render/
│   ├── task8_deploy_on_render.md
│   └── task9_final_validation.md
├── app.py                     # Streamlit entry point (used by Render)
├── run_all.py                 # runs Tasks 1-5 in order
├── Movie_recommendation.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## How it works

1. **Preprocessing (Tasks 1-2):** load the CSV, remove duplicate titles, replace missing values with empty strings, parse genres/keywords from JSON, lowercase, remove punctuation/special characters and stopwords → stored in the `cleantext` column.
2. **TF-IDF (Task 3):** `TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=2)` → matrix of shape `(4800, 5000)`.
3. **Cosine similarity (Task 4):** similarity between every pair of movies → `(4800, 4800)` matrix. Cosine similarity compares the *angle* between vectors rather than their length, so long and short descriptions of the same topic still match, and the 0–1 score is easy to rank.
4. **Recommendation (Task 5):** `recommend(itemname, top_n=5)` finds the movie's index, reads its similarity scores, sorts them and returns the top N (excluding the movie itself).
5. **UI (Task 6):** Streamlit dropdown + Recommend button.
6. **Git, GitHub and Render (Tasks 7-9):** see the `.md` files in `PART5` and `PART6`.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt

python run_all.py                 # Tasks 1-5, prints all outputs
streamlit run app.py              # launch the web app
```

Each task can also be run on its own, for example:

```bash
python PART1_Data_Preprocessing/task1_load_dataset.py
python PART3_Recommendation_Logic/task5_recommend_function.py
```

## Deploy on Render

| Setting | Value |
|---------|-------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |

Full steps are in `PART6_Deployment_on_Render/task8_deploy_on_render.md`.

> On the free plan the app sleeps after inactivity, so the first load can take about a minute.

## Sample output

| Movie | Top recommendations |
|-------|---------------------|
| The Dark Knight | The Dark Knight Rises, Batman Returns, Batman Begins |
| Toy Story | Toy Story 2, Toy Story 3 |
| The Godfather | The Godfather: Part II, Blood Ties, Easy Money |

## Tech stack

Python · Pandas · scikit-learn · Streamlit
