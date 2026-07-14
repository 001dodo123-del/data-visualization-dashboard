"""
Data Visualization Dashboard:-
How it works:-
1. User clicks "Open CSV" and picks a data file.
2. The app reads the column names and lists them in dropdowns.
3. User picks a chart type and the column(s) to plot.
4. User clicks "Generate chart" and the plot appears in the window.
"""

import sys
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("QtAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QFileDialog,
    QMessageBox,
)

sns.set_theme(style="whitegrid")

CHART_TYPES = ["Histogram", "Scatter plot", "Bar chart", "Box plot", "Line chart", "Correlation heatmap"]


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualization Dashboard")
        self.resize(700, 600)

        self.data = None  # holds the loaded CSV as a pandas DataFrame

        # --- Top controls: load file ---
        self.load_button = QPushButton("Open CSV")
        self.load_button.clicked.connect(self.load_csv)

        self.file_label = QLabel("No file loaded")

        top_row = QHBoxLayout()
        top_row.addWidget(self.load_button)
        top_row.addWidget(self.file_label)
        top_row.addStretch()

        # --- Chart controls ---
        self.chart_type_box = QComboBox()
        self.chart_type_box.addItems(CHART_TYPES)
        self.chart_type_box.currentTextChanged.connect(self.update_column_visibility)

        self.x_column_box = QComboBox()
        self.y_column_box = QComboBox()

        controls_row = QHBoxLayout()
        controls_row.addWidget(QLabel("Chart type:"))
        controls_row.addWidget(self.chart_type_box)
        controls_row.addWidget(QLabel("X column:"))
        controls_row.addWidget(self.x_column_box)
        controls_row.addWidget(QLabel("Y column:"))
        controls_row.addWidget(self.y_column_box)

        self.generate_button = QPushButton("Generate chart")
        self.generate_button.clicked.connect(self.generate_chart)

        # --- Matplotlib canvas (this is where the chart is drawn) ---
        self.figure = Figure(figsize=(6, 5))
        self.canvas = FigureCanvas(self.figure)

        # --- Assemble layout ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_row)
        main_layout.addLayout(controls_row)
        main_layout.addWidget(self.generate_button)
        main_layout.addWidget(self.canvas)
        self.setLayout(main_layout)

        self.update_column_visibility(self.chart_type_box.currentText())

    def load_csv(self):
        """Open a file dialog, read the chosen CSV, and populate column dropdowns."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV file", "", "CSV files (*.csv)")
        if not file_path:
            return

        try:
            self.data = pd.read_csv(file_path)
        except Exception as error:
            QMessageBox.critical(self, "Error loading file", str(error))
            return

        self.file_label.setText(file_path.split("/")[-1])

        columns = list(self.data.columns)
        self.x_column_box.clear()
        self.y_column_box.clear()
        self.x_column_box.addItems(columns)
        self.y_column_box.addItems(columns)

    def update_column_visibility(self, chart_type):
        """Histogram, box plot, and heatmap don't need a Y column."""
        needs_y = chart_type in ("Scatter plot", "Line chart")
        self.y_column_box.setEnabled(needs_y)

    def generate_chart(self):
        """Draw the chart the user selected using the loaded data."""
        if self.data is None:
            QMessageBox.warning(self, "No data", "Please load a CSV file first.")
            return

        chart_type = self.chart_type_box.currentText()
        x_column = self.x_column_box.currentText()
        y_column = self.y_column_box.currentText()

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        try:
            if chart_type == "Histogram":
                sns.histplot(data=self.data, x=x_column, kde=True, ax=ax)

            elif chart_type == "Scatter plot":
                sns.scatterplot(data=self.data, x=x_column, y=y_column, ax=ax)

            elif chart_type == "Bar chart":
                sns.barplot(data=self.data, x=x_column, y=y_column, ax=ax)

            elif chart_type == "Box plot":
                sns.boxplot(data=self.data, x=x_column, ax=ax)

            elif chart_type == "Line chart":
                sns.lineplot(data=self.data, x=x_column, y=y_column, ax=ax)

            elif chart_type == "Correlation heatmap":
                numeric_data = self.data.select_dtypes(include="number")
                sns.heatmap(numeric_data.corr(), annot=True, cmap="Blues", ax=ax)

            ax.set_title(chart_type)
            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as error:
            QMessageBox.critical(self, "Error generating chart", str(error))


def main():
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
