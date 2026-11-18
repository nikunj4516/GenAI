# Task 7: Git & GitHub Setup

## 1. Initialize a Git repository

Open a terminal in the project folder `GenAI_Task(20)Nikunj` and run:

```bash
git init
```

## 2. Create a GitHub repository

1. Go to https://github.com/new
2. Repository name: `movie-recommender`
3. Keep it **Public** (Render free tier can read public repos easily)
4. Do **not** tick "Add README" (we already have one)
5. Click **Create repository**

## 3. Commit and push the code

```bash
git add .
git commit -m "Content-based movie recommendation system"
git branch -M main
git remote add origin https://github.com/<your-username>/movie-recommender.git
git push -u origin main
```

## 4. Repository must include

| File | Purpose |
|------|---------|
| `app.py` | Streamlit entry point |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |
| `Movie_recommendation.csv` | Dataset (needed by the deployed app) |
| `PART1_...` to `PART6_...` | Task files |

## 5. Verify

Refresh the GitHub page and confirm all files and folders are visible.

## Updating the project later

```bash
git add .
git commit -m "Describe your change"
git push
```

Render redeploys automatically after every push.
