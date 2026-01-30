import pandas as pd
from io import BytesIO

from django.contrib.auth import authenticate, login
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .serializers import CSVUploadSerializer, DatasetHistorySerializer
from .models import Dataset

from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Disable CSRF check

# =========================
# Constants
# =========================

REQUIRED_COLUMNS = [
    "Equipment Name",
    "Type",
    "Flowrate",
    "Pressure",
    "Temperature",
]


# =========================
# Helper Functions
# =========================

def compute_summary(df):
    return {
        "total_equipment": int(len(df)),
        "average_flowrate": float(df["Flowrate"].mean()),
        "average_pressure": float(df["Pressure"].mean()),
        "average_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict(),
    }


def generate_pdf(dataset):
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    from reportlab.lib.utils import ImageReader
    
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Chemical Equipment Dataset Report")
    y -= 40

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Filename: {dataset.filename}")
    y -= 20
    pdf.drawString(50, y, f"Uploaded At: {dataset.uploaded_at}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Summary Statistics")
    y -= 20

    pdf.setFont("Helvetica", 11)
    summary = dataset.summary

    pdf.drawString(50, y, f"Total Equipment: {summary['total_equipment']}")
    y -= 20
    pdf.drawString(50, y, f"Average Flowrate: {summary['average_flowrate']:.2f}")
    y -= 20
    pdf.drawString(50, y, f"Average Pressure: {summary['average_pressure']:.2f}")
    y -= 20
    pdf.drawString(50, y, f"Average Temperature: {summary['average_temperature']:.2f}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Equipment Type Distribution")
    y -= 20

    pdf.setFont("Helvetica", 11)
    for eq_type, count in summary["type_distribution"].items():
        pdf.drawString(60, y, f"{eq_type}: {count}")
        y -= 18

    # === Generate and embed charts ===
    y -= 20
    
    # Chart 1: Equipment Type Distribution
    type_distribution = summary.get("type_distribution", {})
    if type_distribution:
        fig1, ax1 = plt.subplots(figsize=(5, 3), dpi=100)
        types = list(type_distribution.keys())
        counts = list(type_distribution.values())
        colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336', '#00BCD4']
        bar_colors = [colors[i % len(colors)] for i in range(len(types))]
        ax1.bar(types, counts, color=bar_colors)
        ax1.set_title("Equipment Type Distribution", fontsize=10, fontweight='bold')
        ax1.set_xlabel("Type")
        ax1.set_ylabel("Count")
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout()
        
        # Save chart to BytesIO
        chart1_buffer = BytesIO()
        fig1.savefig(chart1_buffer, format='PNG', dpi=100, bbox_inches='tight')
        chart1_buffer.seek(0)
        plt.close(fig1)
        
        # Embed in PDF
        chart1_img = ImageReader(chart1_buffer)
        pdf.drawImage(chart1_img, 50, y - 200, width=250, height=180)
    
    # Chart 2: Average Parameters
    avg_flowrate = summary.get("average_flowrate", 0)
    avg_pressure = summary.get("average_pressure", 0)
    avg_temperature = summary.get("average_temperature", 0)
    
    fig2, ax2 = plt.subplots(figsize=(5, 3), dpi=100)
    params = ["Flowrate", "Pressure", "Temperature"]
    values = [avg_flowrate, avg_pressure, avg_temperature]
    colors = ['#2196F3', '#4CAF50', '#FF5722']
    ax2.bar(params, values, color=colors)
    ax2.set_title("Average Parameters", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Value")
    for i, (param, value) in enumerate(zip(params, values)):
        ax2.text(i, value + max(values) * 0.02, f"{value:.1f}", ha='center', fontsize=8)
    fig2.tight_layout()
    
    # Save chart to BytesIO
    chart2_buffer = BytesIO()
    fig2.savefig(chart2_buffer, format='PNG', dpi=100, bbox_inches='tight')
    chart2_buffer.seek(0)
    plt.close(fig2)
    
    # Embed in PDF (next to first chart)
    chart2_img = ImageReader(chart2_buffer)
    pdf.drawImage(chart2_img, 310, y - 200, width=250, height=180)

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer



# =========================
# CSRF Token API (GET ONLY)
# =========================

class CSRFTokenAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"message": "CSRF cookie set"})


# =========================
# Login API
# =========================

class LoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)

        return Response(
            {"message": "Login successful"},
            status=status.HTTP_200_OK,
        )

class AuthStatusAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"authenticated": True})

# =========================
# CSV Upload + Analytics API
# (CSRF exempt – multipart safe)
# =========================

class CSVUploadAPIView(GenericAPIView):
    serializer_class = CSVUploadSerializer
    permission_classes = []
    authentication_classes = []
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error": "CSV file is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        csv_file = serializer.validated_data["file"]

        try:
            df = pd.read_csv(csv_file)
        except Exception:
            return Response(
                {"error": "Invalid CSV file."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        missing_columns = [
            col for col in REQUIRED_COLUMNS if col not in df.columns
        ]

        if missing_columns:
            return Response(
                {
                    "error": "Missing required columns.",
                    "missing_columns": missing_columns,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = compute_summary(df)

        Dataset.objects.create(
            filename=csv_file.name,
            summary=summary,
        )

        dataset_ids_to_keep = (
            Dataset.objects
            .order_by("-uploaded_at")
            .values_list("id", flat=True)[:5]
        )

        Dataset.objects.exclude(id__in=dataset_ids_to_keep).delete()

        return Response(
            {
                "message": "CSV uploaded and analyzed successfully.",
                "summary": summary,
            },
            status=status.HTTP_200_OK,
        )


# =========================
# Dataset History API
# =========================

class DatasetHistoryAPIView(GenericAPIView):
    serializer_class = DatasetHistorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Dataset.objects.all().order_by("-uploaded_at")

    def get(self, request):
        datasets = self.get_queryset()[:5]
        serializer = self.get_serializer(datasets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# =========================
# PDF Download API
# =========================

class DatasetPDFAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dataset = Dataset.objects.order_by("-uploaded_at").first()

        if not dataset:
            return Response(
                {"error": "No dataset available."},
                status=status.HTTP_404_NOT_FOUND,
            )

        pdf_buffer = generate_pdf(dataset)

        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=f"{dataset.filename}_report.pdf",
            content_type="application/pdf",
        )
