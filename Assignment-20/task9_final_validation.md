# Task 9: Final Validation

## Deployed app link

```
https://<your-app-name>.onrender.com
```
*(replace with your real Render URL)*

## Validation checklist

| # | Check | Expected | Result |
|---|-------|----------|--------|
| 1 | Open the deployed URL | App loads with title "Movie Recommendation System" | ☐ |
| 2 | Dropdown lists movies | About 4,800 titles, sorted A-Z | ☐ |
| 3 | Select **The Dark Knight** → Recommend | The Dark Knight Rises, Batman Returns, Batman Begins | ☐ |
| 4 | Select **Toy Story** → Recommend | Toy Story 2, Toy Story 3 at the top | ☐ |
| 5 | Select **The Godfather** → Recommend | The Godfather: Part II at the top | ☐ |
| 6 | Change the slider to 10 | 10 recommendations are shown | ☐ |
| 7 | Selected movie is not in its own results | Never appears in the list | ☐ |

## Notes

- The first load after inactivity can be slow (free tier wakes the service).
- If recommendations look wrong, compare with the local output of `python run_all.py`.
