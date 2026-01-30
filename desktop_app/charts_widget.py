"""
Charts Widget for Chemical Equipment Analytics Desktop App

Displays analytics data using Matplotlib charts embedded in PyQt5.
Shows equipment type distribution and average parameters.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartsWidget(QWidget):
    """Widget displaying Matplotlib charts for analytics data."""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Set up the charts container."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create matplotlib figure with 2 subplots
        self.figure = Figure(figsize=(8, 6), dpi=80)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def update_charts(self, summary: dict):
        """Update charts with new analytics data."""
        self.figure.clear()

        # Create 2 subplots (side by side)
        ax1 = self.figure.add_subplot(1, 2, 1)
        ax2 = self.figure.add_subplot(1, 2, 2)

        # Chart 1: Equipment Type Distribution (Bar Chart)
        type_distribution = summary.get("type_distribution", {})
        if type_distribution:
            types = list(type_distribution.keys())
            counts = list(type_distribution.values())
            
            colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336', '#00BCD4']
            bar_colors = [colors[i % len(colors)] for i in range(len(types))]
            
            ax1.bar(types, counts, color=bar_colors)
            ax1.set_title("Equipment Type Distribution", fontsize=10, fontweight='bold')
            ax1.set_xlabel("Type")
            ax1.set_ylabel("Count")
            ax1.tick_params(axis='x', rotation=45)
        else:
            ax1.text(0.5, 0.5, "No data", ha='center', va='center', transform=ax1.transAxes)
            ax1.set_title("Equipment Type Distribution", fontsize=10, fontweight='bold')

        # Chart 2: Average Parameters (Bar Chart)
        avg_flowrate = summary.get("average_flowrate", 0)
        avg_pressure = summary.get("average_pressure", 0)
        avg_temperature = summary.get("average_temperature", 0)

        params = ["Flowrate", "Pressure", "Temperature"]
        values = [avg_flowrate, avg_pressure, avg_temperature]
        colors = ['#2196F3', '#4CAF50', '#FF5722']

        ax2.bar(params, values, color=colors)
        ax2.set_title("Average Parameters", fontsize=10, fontweight='bold')
        ax2.set_ylabel("Value")

        # Add value labels on bars
        for i, (param, value) in enumerate(zip(params, values)):
            ax2.text(i, value + max(values) * 0.02, f"{value:.1f}", ha='center', fontsize=8)

        # Adjust layout
        self.figure.tight_layout()
        self.canvas.draw()

    def clear_charts(self):
        """Clear all charts."""
        self.figure.clear()
        self.canvas.draw()
