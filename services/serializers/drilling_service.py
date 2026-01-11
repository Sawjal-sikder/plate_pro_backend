from rest_framework import serializers #type: ignore
from ..models import DrillingService

class DrillingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrillingService
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]