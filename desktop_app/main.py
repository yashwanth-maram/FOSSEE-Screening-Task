"""
Chemical Equipment Analytics - Desktop Application

Main entry point for the PyQt5 desktop client.
Launches login window first, then opens main application on successful authentication.
"""

import sys
from PyQt5.QtWidgets import QApplication

from login_window import LoginWindow
from upload_window import UploadWindow


class Application:
    """Main application controller."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")
        
        self.login_window = None
        self.main_window = None

    def run(self):
        """Start the application."""
        # Show login window first
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()

        return self.app.exec_()

    def on_login_success(self):
        """Called when login is successful."""
        # Close login window and open main window
        if self.login_window:
            self.login_window.close()
            self.login_window = None

        self.main_window = UploadWindow()
        self.main_window.show()


def main():
    """Entry point."""
    app = Application()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
