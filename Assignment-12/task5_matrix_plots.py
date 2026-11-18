# Task 5: Matrix plots
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# housing.csv should be in the same folder as this file
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "housing.csv")
df = pd.read_csv(file_path)

order = ["INLAND", "<1H OCEAN", "NEAR OCEAN", "NEAR BAY"]

# 1. pair plot - using only 4 columns and 2000 rows, all 9 columns is too much
# ISLAND is removed (5 rows only), a few huge total_rooms values are removed so the
# plots are not squeezed, and value is in thousands so axis numbers dont overlap
small = df[(df["ocean_proximity"] != "ISLAND") & (df["total_rooms"] < 15000)]
small = small.sample(2000, random_state=42).copy()
small["house_value_k"] = small["median_house_value"] / 1000
small = small[["median_income", "housing_median_age", "total_rooms",  "house_value_k", "ocean_proximity"]]

sns.pairplot(small, hue="ocean_proximity", hue_order=order, palette="Set2",height=2.2, plot_kws={"alpha": 0.6, "s": 15})
plt.show()

# 2. heatmap of correlation matrix
# ocean_proximity is text so only the numerical columns are used
corr = df.select_dtypes(include="number").corr()

plt.figure(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation heatmap")
plt.tight_layout()
plt.show()

# Observation:
# median_income and median_house_value have the highest correlation (about 0.69).
# total_rooms, total_bedrooms, population and households are highly correlated
# with each other, which makes sense because bigger areas have all of them more.