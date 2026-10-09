# Task 2: Line plot, scatter style line plot and faceting
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# housing.csv should be in the same folder as this file
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "housing.csv")
df = pd.read_csv(file_path)

# ISLAND has only 5 rows so a line for it makes no sense, removing it here
df = df[df["ocean_proximity"] != "ISLAND"]
order = ["INLAND", "<1H OCEAN", "NEAR OCEAN", "NEAR BAY"]

# 1. simple line plot (shaded area is the confidence interval)
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x="housing_median_age", y="median_house_value",hue="ocean_proximity", hue_order=order, palette="Set2", err_kws={"alpha": 0.1})
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
plt.title("Average house value by housing age")
plt.tight_layout()
plt.show()

# 2. same thing with markers so it looks like scatter + line
plt.figure(figsize=(10, 5))
sns.lineplot(data=df, x="housing_median_age", y="median_house_value", hue="ocean_proximity", hue_order=order, palette="Set2", marker="o", err_style=None)
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
plt.title("Line plot with markers")
plt.tight_layout()
plt.show()

# 3. faceting - one small plot for each ocean_proximity
g = sns.relplot(data=df, x="housing_median_age", y="median_house_value",  col="ocean_proximity", col_order=order, col_wrap=2,  hue="ocean_proximity", hue_order=order, palette="Set2",   kind="line", marker="o", legend=False, height=3.5, aspect=1.4)
g.set_titles("{col_name}")
plt.show()

# Observation:
# age doesnt change the price much. INLAND prices go down a little as age increases.
# faceting makes it easier to compare because lines are not on top of each other.