"""
API Client for Chemical Equipment Analytics Desktop App

Uses requests.Session() to maintain cookies across requests.
Handles CSRF token fetching and attachment automatically.
"""

import os
import requests
from typing import Optional, Dict, Any, Tuple


class APIClient:
    """
    Reusable API client that maintains session cookies.
    All windows share the same instance of this client.
    """

    # Use environment variable for API URL, fallback to localhost for development
    BASE_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

    def __init__(self):
        self.session = requests.Session()
        self._csrf_token: Optional[str] = None

    def _get_csrf_token(self) -> str:
        """Fetch CSRF token from the backend and store it."""
        response = self.session.get(f"{self.BASE_URL}/api/csrf/")
        response.raise_for_status()
        
        # Extract CSRF token from cookies
        self._csrf_token = self.session.cookies.get("csrftoken")
        return self._csrf_token or ""

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with CSRF token for POST requests."""
        if not self._csrf_token:
            self._get_csrf_token()
        
        return {
            "X-CSRFToken": self._csrf_token or "",
            "Referer": self.BASE_URL,
        }

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate with the backend.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Ensure we have a fresh CSRF token
            self._get_csrf_token()

            response = self.session.post(
                f"{self.BASE_URL}/api/login/",
                json={"username": username, "password": password},
                headers=self._get_headers(),
            )

            if response.status_code == 200:
                return True, "Login successful"
            elif response.status_code == 401:
                return False, "Invalid credentials"
            else:
                data = response.json()
                return False, data.get("error", "Login failed")

        except requests.RequestException as e:
            return False, f"Connection error: {str(e)}"

    def upload_csv(self, file_path: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Upload a CSV file and get analytics.
        
        Note: This endpoint is unauthenticated per backend design.
        
        Returns:
            Tuple of (success: bool, data: dict with analytics or error)
        """
        try:
            with open(file_path, "rb") as f:
                files = {"file": (file_path.split("\\")[-1].split("/")[-1], f, "text/csv")}
                response = self.session.post(
                    f"{self.BASE_URL}/api/upload-csv/",
                    files=files,
                )

            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json()

        except requests.RequestException as e:
            return False, {"error": f"Connection error: {str(e)}"}
        except FileNotFoundError:
            return False, {"error": "File not found"}

    def get_history(self) -> Tuple[bool, Any]:
        """
        Get the last 5 datasets.
        
        Returns:
            Tuple of (success: bool, data: list of datasets or error dict)
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/api/history/",
                headers=self._get_headers(),
            )

            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 403:
                return False, {"error": "Authentication required"}
            else:
                return False, {"error": f"Failed to load history (status {response.status_code})"}

        except requests.RequestException as e:
            return False, {"error": f"Connection error: {str(e)}"}

    def download_pdf(self, save_path: str) -> Tuple[bool, str]:
        """
        Download the latest PDF report.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/api/pdf/",
                headers=self._get_headers(),
                stream=True,
            )

            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True, f"PDF saved to {save_path}"
            elif response.status_code == 403:
                return False, "Authentication required"
            elif response.status_code == 404:
                return False, "No dataset available"
            else:
                return False, f"Failed to download PDF (status {response.status_code})"

        except requests.RequestException as e:
            return False, f"Connection error: {str(e)}"


# Singleton instance shared across all windows
api_client = APIClient()
