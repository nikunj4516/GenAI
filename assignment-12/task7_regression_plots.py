# Task 7: Regression plots
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# housing.csv should be in the same folder as this file
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "housing.csv")
df = pd.read_csv(file_path)

order = ["INLAND", "<1H OCEAN", "NEAR OCEAN", "NEAR BAY"]

# sample to keep the plots light, ISLAND removed (only 5 rows)
data = df[df["ocean_proximity"] != "ISLAND"].sample(5000, random_state=42)

# 1. regplot between two numerical columns
plt.figure(figsize=(8, 5))
sns.regplot(data=data, x="median_income", y="median_house_value", scatter_kws={"alpha": 0.3, "s": 10}, line_kws={"color": "red"})
plt.ylim(0, 520000)   # house value is capped at 500001 so no point showing more
plt.title("Regplot: income vs house value")
plt.show()

# 2. lmplot with hue (separate line for each category)
g = sns.lmplot(data=data, x="median_income", y="median_house_value", hue="ocean_proximity", hue_order=order, palette="Set2",  height=5, aspect=1.4, scatter_kws={"alpha": 0.5, "s": 10})
g.set(ylim=(0, 520000))
plt.title("Lmplot with hue = ocean_proximity")
plt.show()

# Observation:
# line goes up, so income is a good thing to predict house value.
# the lines for each category have different slope, so location also matters.