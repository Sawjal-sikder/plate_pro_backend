from rest_framework import serializers #type: ignore
from services.models import DrillingArea

class DrillingAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrillingArea
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]