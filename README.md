# Data Visualization Dashboard

A simple desktop dashboard that lets you load your own CSV file and
turn it into charts using seaborn and matplotlib — no coding required
to use it.

## What it does

1. Click **Open CSV** and pick any CSV file from your computer.
2. The app reads the column names and lists them in dropdowns.
3. Choose a chart type and the column(s) you want to plot.
4. Click **Generate chart** and the chart appears right in the window.

## Supported chart types

| Chart type | Needs X column | Needs Y column | Good for |
|---|---|---|---|
| Histogram | Yes | No | Distribution of one numeric column |
| Scatter plot | Yes | Yes | Relationship between two numeric columns |
| Bar chart | Yes | Yes | Comparing values across categories |
| Box plot | Yes | No | Spread and outliers in one numeric column |
| Line chart | Yes | Yes | Trends over an ordered column (e.g. time) |
| Correlation heatmap | - | - | Correlation between all numeric columns |

## Requirements

- Python 3.9+
- PySide6
- pandas
- seaborn
- matplotlib

## Setup

1. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the app:

```bash
python main.py
```

Then load any CSV file with numeric or categorical columns and start
exploring it visually.

## How the code is organized

`main.py` has one class, `Dashboard`, split into small, focused methods:

- `load_csv()` — opens the file picker and reads the CSV into a pandas
  DataFrame.
- `update_column_visibility()` — disables the Y column dropdown for
  chart types that don't need it.
- `generate_chart()` — the core logic: clears the old chart, then
  calls the matching seaborn function based on the selected chart
  type, and redraws the canvas.

## Project Structure

```
data_viz_dashboard/
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```
