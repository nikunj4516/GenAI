# Task 1: Relational plot
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# housing.csv should be in the same folder as this file
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "housing.csv")
df = pd.read_csv(file_path)

# only 207 values missing in total_bedrooms so filling with median
df["total_bedrooms"] = df["total_bedrooms"].fillna(df["total_bedrooms"].median())

# same order of categories in every plot so colors stay same
order = ["INLAND", "<1H OCEAN", "NEAR OCEAN", "NEAR BAY", "ISLAND"]

# taking a sample, 20000 points makes the plot too crowded
data = df.sample(5000, random_state=42)

# 1. relplot -> x and y both numerical, hue is the categorical column
sns.relplot(data=data, x="median_income", y="median_house_value",  hue="ocean_proximity", hue_order=order, palette="Set2",  alpha=0.6, height=5, aspect=1.4)
plt.title("Median income vs house value")
plt.show()

# 2. same plot but using scatter style
plt.figure(figsize=(9, 5))
sns.scatterplot(data=data, x="median_income", y="median_house_value",  hue="ocean_proximity", hue_order=order, palette="Set2", style="ocean_proximity", style_order=order, alpha=0.6)
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
plt.title("Scatterplot: income vs house value")
plt.tight_layout()
plt.show()

# Observation:
# higher income -> higher house value. INLAND houses are mostly at the bottom.
# the flat line at the top is because house value is capped at 500001.