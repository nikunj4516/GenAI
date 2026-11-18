# Task 6: Categorical plots (ocean_proximity and median_house_value)
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# housing.csv should be in the same folder as this file
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "housing.csv")
df = pd.read_csv(file_path)

# fixed order so every plot has same order and colors
order = ["INLAND", "<1H OCEAN", "NEAR OCEAN", "NEAR BAY", "ISLAND"]

# 1. bar plot - shows the average house value of each category
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="ocean_proximity", y="median_house_value", order=order,  hue="ocean_proximity", hue_order=order, palette="Set2", legend=False)
plt.title("Bar plot: average house value")
plt.show()

# 2. box plot
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="ocean_proximity", y="median_house_value", order=order,   hue="ocean_proximity", hue_order=order, palette="Set2", legend=False)
plt.title("Box plot")
plt.show()

# 3. violin plot (cut=0 so it doesnt go below 0 or above the max value)
plt.figure(figsize=(8, 5))
sns.violinplot(data=df, x="ocean_proximity", y="median_house_value", order=order,  hue="ocean_proximity", hue_order=order, palette="Set2",  legend=False, cut=0)
plt.title("Violin plot")
plt.show()

# 4. count plot - how many rows in each category
plt.figure(figsize=(8, 5))
ax = sns.countplot(data=df, x="ocean_proximity", order=order,  hue="ocean_proximity", hue_order=order, palette="Set2", legend=False)
for bars in ax.containers:
    ax.bar_label(bars)    # writes the count on top of the bar
plt.title("Count plot")
plt.show()

# Observation:
# INLAND has the lowest house values (average is around 125k).
# the other categories are around 240k to 260k.
# ISLAND has only 5 rows so we cant say much about it.