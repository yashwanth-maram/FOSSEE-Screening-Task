"""
Upload Window for Chemical Equipment Analytics Desktop App
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QGroupBox,
    QMessageBox,
    QTabWidget,
)
from PyQt5.QtCore import Qt

from api_client import api_client
from history_widget import HistoryWidget
from charts_widget import ChartsWidget


class UploadWindow(QWidget):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Analytics")
        self.setMinimumSize(700, 800)
        self.selected_file = None
        self.current_summary = None
        self.setup_ui()
        self.load_initial_data()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("Chemical Equipment Analytics")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Upload Section
        upload_group = QGroupBox("Upload CSV")
        upload_layout = QVBoxLayout()

        # File selection
        file_row = QHBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: gray;")
        file_row.addWidget(self.file_label, stretch=1)
        
        browse_button = QPushButton("Browse...")
        browse_button.setFixedWidth(100)
        browse_button.clicked.connect(self.browse_file)
        file_row.addWidget(browse_button)
        
        upload_layout.addLayout(file_row)

        # Upload button
        self.upload_button = QPushButton("Upload CSV")
        self.upload_button.clicked.connect(self.upload_csv)
        self.upload_button.setEnabled(False)
        upload_layout.addWidget(self.upload_button)

        upload_group.setLayout(upload_layout)
        main_layout.addWidget(upload_group)

        # Analytics Section
        analytics_group = QGroupBox("Analytics")
        analytics_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        # Summary Tab
        summary_tab = QWidget()
        summary_layout = QVBoxLayout()
        self.analytics_text = QTextEdit()
        self.analytics_text.setReadOnly(True)
        self.analytics_text.setPlaceholderText("Upload a CSV to see analytics...")
        self.analytics_text.setMinimumHeight(200)
        summary_layout.addWidget(self.analytics_text)
        summary_tab.setLayout(summary_layout)
        self.tab_widget.addTab(summary_tab, "Summary")

        # Charts Tab
        charts_tab = QWidget()
        charts_layout = QVBoxLayout()
        self.charts_widget = ChartsWidget()
        charts_layout.addWidget(self.charts_widget)
        charts_tab.setLayout(charts_layout)
        self.tab_widget.addTab(charts_tab, "Charts")

        analytics_layout.addWidget(self.tab_widget)
        analytics_group.setLayout(analytics_layout)
        main_layout.addWidget(analytics_group)

        # History Section
        history_group = QGroupBox("History")
        history_layout = QVBoxLayout()
        self.history_widget = HistoryWidget()
        history_layout.addWidget(self.history_widget)
        history_group.setLayout(history_layout)
        main_layout.addWidget(history_group)

        # PDF Download
        pdf_layout = QHBoxLayout()
        pdf_layout.addStretch()
        
        self.pdf_button = QPushButton("Download Latest PDF Report")
        self.pdf_button.setFixedWidth(220)
        self.pdf_button.clicked.connect(self.download_pdf)
        pdf_layout.addWidget(self.pdf_button)
        
        pdf_layout.addStretch()
        main_layout.addLayout(pdf_layout)

        self.setLayout(main_layout)

    def load_initial_data(self):
        self.history_widget.load_history()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )

        if file_path:
            self.selected_file = file_path
            filename = file_path.split("\\")[-1].split("/")[-1]
            self.file_label.setText(filename)
            self.file_label.setStyleSheet("color: black;")
            self.upload_button.setEnabled(True)

    def upload_csv(self):
        if not self.selected_file:
            return

        self.upload_button.setEnabled(False)
        self.upload_button.setText("Uploading...")
        self.analytics_text.clear()

        success, data = api_client.upload_csv(self.selected_file)

        self.upload_button.setEnabled(True)
        self.upload_button.setText("Upload CSV")

        if success:
            summary = data.get("summary", {})
            self.current_summary = summary
            self.display_analytics(summary)
            self.charts_widget.update_charts(summary)
            self.tab_widget.setCurrentIndex(1)
            self.history_widget.load_history()
            
            self.selected_file = None
            self.file_label.setText("No file selected")
            self.file_label.setStyleSheet("color: gray;")
            self.upload_button.setEnabled(False)
        else:
            error_msg = data.get("error", "Upload failed")
            missing = data.get("missing_columns", [])
            if missing:
                error_msg += f"\nMissing columns: {', '.join(missing)}"
            QMessageBox.warning(self, "Upload Error", error_msg)

    def display_analytics(self, summary: dict):
        lines = [
            "=== Analytics Summary ===",
            "",
            f"Total Equipment: {summary.get('total_equipment', 'N/A')}",
            "",
            "--- Averages ---",
        ]
        
        avg_flowrate = summary.get('average_flowrate', 'N/A')
        avg_pressure = summary.get('average_pressure', 'N/A')
        avg_temp = summary.get('average_temperature', 'N/A')
        
        lines.append(f"  Flowrate:    {avg_flowrate:.2f}" if isinstance(avg_flowrate, (int, float)) else f"  Flowrate:    {avg_flowrate}")
        lines.append(f"  Pressure:    {avg_pressure:.2f}" if isinstance(avg_pressure, (int, float)) else f"  Pressure:    {avg_pressure}")
        lines.append(f"  Temperature: {avg_temp:.2f}" if isinstance(avg_temp, (int, float)) else f"  Temperature: {avg_temp}")
        
        lines.extend(["", "--- Type Distribution ---"])

        type_dist = summary.get("type_distribution", {})
        for eq_type, count in type_dist.items():
            lines.append(f"  {eq_type}: {count}")

        self.analytics_text.setText("\n".join(lines))

    def download_pdf(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", "equipment_report.pdf", "PDF Files (*.pdf);;All Files (*)"
        )

        if not save_path:
            return

        self.pdf_button.setEnabled(False)
        self.pdf_button.setText("Downloading...")

        success, message = api_client.download_pdf(save_path)

        self.pdf_button.setEnabled(True)
        self.pdf_button.setText("Download Latest PDF Report")

        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Download Error", message)
