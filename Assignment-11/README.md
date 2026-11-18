# Assignment 11 - Matplotlib

## Subject
Matplotlib (Core Plot Types & Visualization)

## Dataset
sales_data.csv (51,290 orders, 2011-2014)

## Tasks Included

1. Line Plot (Sales Trend)
2. Scatter Plot (Sales vs Profit)
3. Bar Plot (Vertical & Horizontal)
4. Multiple Bar Plot (Sales of Different Years)
5. Stacked Bar Chart
6. Histogram (Sales Distribution)
7. Pie Chart (Category Share)

## Requirements

Install Matplotlib:

pip install matplotlib

Install Pandas (used only to read the CSV and group the data, not for plotting):

pip install pandas

Install NumPy:

pip install numpy

## How to Run

1. Keep all the .py files and sales_data.csv in the same folder.

2. Open a terminal in that folder:

cd path/to/assignment_11

3. Run each task file one by one:

python task1_line_plot.py

python task2_scatter_plot.py

python task3_bar_plot.py

python task4_multiple_bar_plot.py

python task5_stacked_bar_chart.py

python task6_histogram.py

python task7_pie_chart.py

4. A plot window opens for each task. Close the window to finish the file
(Task 3 shows two plots, one after the other).

5. Each plot is also saved as a .png image in the same folder.

Note: use python3 instead of python on macOS/Linux if needed.

## Troubleshooting

FileNotFoundError / "sales_data.csv not found":
the CSV must be in the same folder as the .py files. Each file looks for
sales_data.csv next to itself, so it works even if you run it from another
folder (for example with the VS Code run button), but the CSV must be
placed beside the .py files.

ModuleNotFoundError: install the missing library with
pip install pandas matplotlib numpy

## Output Files

| Task | Image Saved |
|------|-------------|
| 1 | task1_line_plot.png |
| 2 | task2_scatter_plot.png |
| 3 | task3_bar_vertical.png, task3_bar_horizontal.png |
| 4 | task4_multiple_bar.png |
| 5 | task5_stacked_bar.png |
| 6 | task6_histogram.png |
| 7 | task7_pie_chart.png |

## Notes

- Only matplotlib.pyplot is used for plotting.
- No Seaborn and no Pandas plotting (DataFrame.plot).
- The sales column has commas in large values (e.g. "1,648"), so they are removed before converting to numbers.
- The CSV is read with encoding="cp1252".
- Plots are kept simple, with title and axis labels on every plot (legend on Tasks 4 and 5, percentages on Task 7).

Author : 
Nikunj
