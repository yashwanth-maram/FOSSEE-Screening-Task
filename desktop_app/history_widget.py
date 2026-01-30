"""
History Widget for Chemical Equipment Analytics Desktop App
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
)
from PyQt5.QtCore import Qt
from datetime import datetime

from api_client import api_client


def format_local_time(iso_string):
    """Convert ISO timestamp to local timezone readable format."""
    try:
        if iso_string.endswith('Z'):
            iso_string = iso_string[:-1] + '+00:00'
        dt = datetime.fromisoformat(iso_string)
        local_dt = dt.astimezone()
        return local_dt.strftime("%Y-%m-%d %H:%M")
    except:
        return iso_string


class HistoryWidget(QWidget):
    """Widget displaying upload history (last 5 datasets)."""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Upload History")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFixedWidth(80)
        self.refresh_button.clicked.connect(self.load_history)
        header_layout.addWidget(self.refresh_button)
        
        layout.addLayout(header_layout)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()
        layout.addWidget(self.error_label)

        # History list
        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(150)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def load_history(self):
        self.list_widget.clear()
        self.error_label.hide()
        self.refresh_button.setEnabled(False)
        self.refresh_button.setText("Loading...")

        success, data = api_client.get_history()

        self.refresh_button.setEnabled(True)
        self.refresh_button.setText("Refresh")

        if success:
            if not data:
                item = QListWidgetItem("No datasets uploaded yet")
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                self.list_widget.addItem(item)
            else:
                for dataset in data:
                    filename = dataset.get("filename", "Unknown")
                    uploaded_at = dataset.get("uploaded_at", "")
                    formatted_time = format_local_time(uploaded_at)
                    
                    item_text = f"{filename} — {formatted_time}"
                    self.list_widget.addItem(item_text)
        else:
            error_msg = data.get("error", "Failed to load history")
            self.error_label.setText(error_msg)
            self.error_label.show()
