from rest_framework import serializers
from .models import Dataset

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
class DatasetHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "filename", "uploaded_at", "summary"]