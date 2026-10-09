# Task 3: Distribution plots (median_income column)
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# housing.csv should be in the same folder as this file
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "housing.csv")
df = pd.read_csv(file_path)

# 1. histogram
plt.figure(figsize=(7, 4))
sns.histplot(df["median_income"], bins=40)
plt.title("Histogram of median income")
plt.show()

# 2. kde plot
plt.figure(figsize=(7, 4))
sns.kdeplot(df["median_income"], fill=True, cut=0)
plt.title("KDE plot of median income")
plt.show()

# 3. rug plot (small sample otherwise the lines get too thick)
plt.figure(figsize=(7, 2.5))
sns.rugplot(df["median_income"].sample(300, random_state=1), height=0.5, alpha=0.4)
plt.yticks([])   # y axis has no meaning in a rug plot
plt.title("Rug plot of median income")
plt.show()

# 4. histogram and kde together
plt.figure(figsize=(7, 4))
sns.histplot(df["median_income"], bins=40, kde=True)
plt.title("Histogram + KDE")
plt.show()

# Observation:
# income is right skewed, most districts are between 2 and 5.
# there are few very high values, and a small bar at 15 because the data is capped there.