# Task 8: Deploy Application on Render

## Steps

1. Create an account at https://render.com (sign up with GitHub for the easiest setup).
2. Connect Render with GitHub: **Account Settings → GitHub → Connect**, and allow access to the `movie-recommender` repository.
3. Click **New +** → **Web Service**.
4. Select the `movie-recommender` repository.
5. Configure the service:

| Setting | Value |
|---------|-------|
| Name | `movie-recommender` |
| Region | Closest to you (e.g. Singapore) |
| Branch | `main` |
| Root Directory | *(leave empty)* |
| Runtime / Language | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |
| Instance Type | `Free` |

6. Click **Create Web Service**.
7. Wait for the logs to show the service as **Live** (first build takes a few minutes).

## Notes

- If the build fails because of the Python version, add an environment variable `PYTHON_VERSION` = `3.11.9`.
- Free instances sleep after inactivity, so the first visit may take around a minute.
- The similarity matrix is stored as `float32` so the app fits in the 512 MB free-tier memory.

## Deployed URL

```
https://<your-app-name>.onrender.com
```
