# Assignment 13 - Data Gathering, Preprocessing & EDA

## Subject

Data Gathering (CSV, JSON, SQL, API), Data Preprocessing & Cleaning and Exploratory Data Analysis (EDA) using Pandas, NumPy, Matplotlib, Seaborn, Requests and SQLite.

No Machine Learning model is trained in this assignment.

---

## Dataset

train.csv (Processed Titanic Dataset)

Dataset contains passenger information and survival details.

### Important Columns

- Passengerid
- Age
- Fare
- Sex
- sibsp
- Parch
- Pclass
- Embarked
- 2urvived

### Target Column

```text
2urvived

0 = Did Not Survive
1 = Survived
```

### Dataset Notes

- Most columns are already numerical.
- Sex is already encoded.
- Embarked is already encoded.
- Multiple unnecessary columns named "zero" are present.
- Those columns are removed during preprocessing.

### Additional Files Created During Assignment

```text
products.json
sample.db
tmdb_movies.csv
titanic_clean.csv
titanic_features_X.csv
titanic_target_y.csv
```

---

## Tasks Included

### Part 1 - Data Gathering

### Task 1

Load Data from CSV

- Load train.csv using Pandas
- Print dataset shape
- Print column names
- Print first 5 rows

### Task 2

Load Data from JSON

- Create products.json
- Load JSON file
- Convert into DataFrame
- Display DataFrame

### Task 3

Load Data from SQL Database

- Create SQLite database
- Create employees table
- Insert employee records
- Read data using SQL query
- Convert result into DataFrame

### Task 4

TMDB API Movie Data Collector

- Generate TMDB API Key
- Collect popular movie data
- Extract important fields
- Convert API response into DataFrame
- Save as tmdb_movies.csv

---

### Part 2 - Data Preprocessing & Cleaning

### Task 5

Understanding the Data

- Dataset Shape
- Data Types
- Numerical Columns
- Categorical Columns
- Missing Values

### Task 6

Data Cleaning

- Remove duplicate rows
- Handle missing values
- Remove unnecessary columns
- Rename columns
- Fix data types

### Task 7

Feature Preparation

- Separate Features (X)
- Separate Target (y)
- Save processed files

---

### Part 3 - Exploratory Data Analysis (EDA)

### Task 8

Univariate Analysis

- Histogram
- Histogram with KDE
- Count Plot
- Box Plot
- Violin Plot
- Pie Chart
- Distribution Analysis

### Task 9

Bivariate Analysis

Numerical vs Numerical

- Scatter Plot

Correlation Analysis

- Heatmap

Categorical vs Numerical

- Bar Plot
- Box Plot

Multivariate

- Pair Plot

### Task 10

Insights & Observations

- Data Quality Issues
- Patterns
- Relationships
- Outliers
- Key Findings

---

## Requirements

Install Pandas

```bash
pip install pandas
```

Install NumPy

```bash
pip install numpy
```

Install Matplotlib

```bash
pip install matplotlib
```

Install Seaborn

```bash
pip install seaborn
```

Install Requests

```bash
pip install requests
```

SQLite (sqlite3) and JSON are included with Python.

No installation required.

---

## TMDB API Key (Task 4)

Create a free account:

https://www.themoviedb.org

Generate API Key from:

```text
Settings -> API
```

### Windows PowerShell

```powershell
setx TMDB_API_KEY "your_api_key"
```

Restart terminal after setting the variable.

### macOS / Linux

```bash
export TMDB_API_KEY="your_api_key"
```

If API key is missing, only Task 4 will be skipped.

All other tasks will work normally.

---

## Project Structure

```text
Assignment13/

│
├── train.csv
│
├── Task1_load_csv.py
├── Task2_load_json.py
├── Task3_load_sql.py
├── Task4_tmdb_api.py
├── Task5_understanding_data.py
├── Task6_data_cleaning.py
├── Task7_feature_preparation.py
├── Task8_univariate_analysis.py
├── Task9_bivariate_analysis.py
├── Task10_insights.py
│
├── products.json
├── sample.db
├── tmdb_movies.csv
├── titanic_clean.csv
├── titanic_features_X.csv
├── titanic_target_y.csv
│
├── screenshots/
│
└── README.md
```

---

## How To Run

### Step 1

Place all Python files and train.csv inside the same folder.

### Step 2

Open terminal in project folder

```bash
cd path/to/Assignment13
```

### Step 3

Run files one by one

```bash
python Task1_load_csv.py

python Task2_load_json.py

python Task3_load_sql.py

python Task4_tmdb_api.py

python Task5_understanding_data.py

python Task6_data_cleaning.py

python Task7_feature_preparation.py

python Task8_univariate_analysis.py

python Task9_bivariate_analysis.py

python Task10_insights.py
```

Note:

```text
Use python3 instead of python on Linux or macOS if required.
```

---

## Output Files Generated

### Task 2

```text
products.json
```

### Task 3

```text
sample.db
```

### Task 4

```text
tmdb_movies.csv
```

### Task 6

```text
titanic_clean.csv
```

### Task 7

```text
titanic_features_X.csv

titanic_target_y.csv
```

---

## Visualizations Generated

### Task 8 - Univariate Analysis

```text
Age Histogram

Age Histogram + KDE

Fare Histogram

Fare Histogram + KDE

Sex Count Plot

Age Box Plot

Fare Box Plot

Age Violin Plot

Survival Pie Chart
```

### Task 9 - Bivariate Analysis

```text
Age vs Fare Scatter Plot

Age vs Survival Box Plot

Fare vs Survival Box Plot

Sex vs Survival Bar Plot

Pclass vs Survival Bar Plot

Correlation Heatmap

Pair Plot
```

---

## Troubleshooting

### train.csv not found

```text
Place train.csv inside the same folder as the Python files.
```

---

### TMDB_API_KEY not found

```text
Set environment variable and restart terminal.
```

---

### 401 Unauthorized

```text
API key is invalid or expired.
Generate a new TMDB API Key.
```

---

### ModuleNotFoundError

Install missing packages

```bash
pip install pandas numpy matplotlib seaborn requests
```

---

### Plot window does not close

```text
Close current graph window.
Next graph will open automatically.
```

---

## Observations

### Task 1

Dataset loads successfully into a Pandas DataFrame.

### Task 2

JSON data can be converted directly into a DataFrame.

### Task 3

SQL query output can be loaded into Pandas using read_sql_query().

### Task 4

API response is converted into tabular structure and saved as CSV.

### Task 5

Most columns are numerical.

Target column:

```text
2urvived
```

Several unnecessary columns named:

```text
zero
```

require cleaning.

### Task 6

Missing Age values are replaced using median.

Duplicate rows are removed.

Unnecessary columns are dropped.

### Task 7

Features and target are separated successfully.

### Task 8

Fare contains large outliers.

Age mostly lies between 20 and 40.

### Task 9

Sex and Passenger Class show strong influence on survival.

### Task 10

EDA reveals useful relationships before machine learning.

---

## Key Insights

### Insight 1

Fare contains significant outliers.

### Insight 2

Most passengers belong to the age range of 20 to 40 years.

### Insight 3

Female passengers show higher survival rates.

### Insight 4

First-class passengers survive more often than lower classes.

### Insight 5

Passenger class and fare are strongly related.

### Insight 6

Age contains missing values and requires preprocessing.

### Insight 7

Family related attributes affect survival.

### Insight 8

Removing unnecessary columns improves data quality.

### Insight 9

Younger passengers appear to have slightly better survival rates.

### Insight 10

EDA helps identify trends before machine learning.

---

## Restrictions Followed

```text
✓ Pandas

✓ NumPy

✓ Matplotlib

✓ Seaborn

✓ Requests

✓ SQLite

✗ No Machine Learning Models

✗ No Logistic Regression

✗ No Decision Tree

✗ No Random Forest

✗ No XGBoost
```

---

## Notes

- Only Pandas, NumPy, Matplotlib, Seaborn, Requests and SQLite are used.
- No machine learning model is trained.
- Every task is independent.
- Tasks 7, 8, 9 and 10 use cleaned data from Task 6.
- Median is used for missing Age values because it is robust to outliers.
- Fare contains significant outliers.
- All preprocessing is completed before EDA.
- Do not share your TMDB API Key publicly.

---

## Author

```text
Nikunj Bariya
```
