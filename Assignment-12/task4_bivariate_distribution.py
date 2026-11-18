# Task 4: Bivariate distribution plots
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# housing.csv should be in the same folder as this file
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "housing.csv")
df = pd.read_csv(file_path)

# 1. bivariate histogram
plt.figure(figsize=(7, 5))
sns.histplot(data=df, x="median_income", y="median_house_value", bins=40, cbar=True)
plt.title("Bivariate histogram")
plt.show()

# 2. bivariate kde (using a sample so it runs faster)
# cut=0 so the shape stops at the real data (no negative house values)
plt.figure(figsize=(7, 5))
sns.kdeplot(data=df.sample(8000, random_state=42), x="median_income",  y="median_house_value", fill=True, cut=0)
plt.title("Bivariate KDE")
plt.show()

# Observation:
# most of the data is around income 2 to 5 and house value 100k to 250k.
# the shape goes upwards, so more income means more house value.