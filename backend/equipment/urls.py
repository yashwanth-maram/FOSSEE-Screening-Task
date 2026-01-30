from django.urls import path
from .views import (
    CSVUploadAPIView,
    DatasetHistoryAPIView,
    DatasetPDFAPIView,
    LoginAPIView,
    CSRFTokenAPIView,
    AuthStatusAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("upload-csv/", CSVUploadAPIView.as_view(), name="upload-csv"),
    path("history/", DatasetHistoryAPIView.as_view(), name="dataset-history"),
    path("pdf/", DatasetPDFAPIView.as_view(), name="dataset-pdf"),
    path("csrf/", CSRFTokenAPIView.as_view(), name="csrf"),
    path("auth-status/", AuthStatusAPIView.as_view(), name="auth-status"),
]
