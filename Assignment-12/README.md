# Assignment 12 - Seaborn

## Subject
Seaborn (Relational, Distribution, Categorical, Regression, Matrix Plots & Faceting)

## Dataset
housing.csv (California Housing Prices from Kaggle, 20,640 districts, 10 columns)

- Numerical columns: longitude, latitude, housing_median_age, total_rooms,
  total_bedrooms, population, households, median_income, median_house_value
- Categorical column: ocean_proximity (INLAND, <1H OCEAN, NEAR OCEAN, NEAR BAY, ISLAND)

## Tasks Included

1. Relational Plot (relplot + scatter style)
2. Line Plot as Scatter & Facet
3. Distribution Plots (Histogram, KDE, Rug, Histogram + KDE)
4. Bivariate Distribution Plots (Bivariate Histogram & KDE)
5. Matrix Plots (Pair Plot & Correlation Heatmap)
6. Categorical Plots (Bar, Box, Violin, Count)
7. Regression Plots (regplot & lmplot with hue)
8. Bonus: Faceting & Multi-plots (FacetGrid, subplots, jointplot)

## Requirements

Install Seaborn:

pip install seaborn

Install Pandas (used to load the CSV and prepare the data):

pip install pandas

Install Matplotlib:

pip install matplotlib

## How to Run

1. Keep all the .py files and housing.csv in the same folder.

2. Open a terminal in that folder:

cd path/to/assignment_12

3. Run each task file one by one:

python task1_relational_plot.py

python task2_line_plot_facet.py

python task3_distribution_plots.py

python task4_bivariate_distribution.py

python task5_matrix_plots.py

python task6_categorical_plots.py

python task7_regression_plots.py

python bonus_faceting_multiplots.py

4. A plot window opens for each plot. Close the window to see the next one
(Task 1 shows 2 plots, Task 2 shows 3, Task 3 shows 4, Task 4 shows 2,
Task 5 shows 2, Task 6 shows 4, Task 7 shows 2, Bonus shows 3).

Note: use python3 instead of python on macOS/Linux if needed.

## Troubleshooting

FileNotFoundError / "housing.csv not found":
the CSV must be in the same folder as the .py files. Each file looks for
housing.csv next to itself, so it works even if you run it from another
folder (for example with the VS Code run button), but the CSV must be
placed beside the .py files.

ModuleNotFoundError: install the missing library with
pip install pandas seaborn matplotlib

## Observations

- Task 1: higher median_income means higher house value. INLAND districts are
  mostly at the bottom.
- Task 2: housing age does not change the price much. INLAND prices go down
  a little as age increases. Faceting makes each category easy to see.
- Task 3: median_income is right skewed. Most districts are between 2 and 5.
- Task 4: most data is around income 2 to 5 and house value 100k to 250k.
- Task 5: median_income has the highest correlation with median_house_value
  (about 0.69). total_rooms, total_bedrooms, population and households are
  highly correlated with each other.
- Task 6: INLAND has the lowest house values (average about 125k). The other
  categories are around 240k to 260k.
- Task 7: the regression line goes up, so income is a good predictor of house
  value. The slope is different for each category.

## Notes

- Only Seaborn, Pandas and Matplotlib are used. No Plotly or other
  visualization library.
- total_bedrooms has 207 missing values, they are filled with the median.
- Scatter, pair and regression plots use a random sample (2000 to 5000 rows)
  because 20,000 points make the plot too crowded.
- The ISLAND category has only 5 rows, so it is removed from the line plots,
  pair plot and regression plots.
- median_house_value is capped at 500001, that is why a flat line of points
  appears at the top of many plots.
- The same order and colors of the categories are used in every plot.

Author : 
Nikunj

