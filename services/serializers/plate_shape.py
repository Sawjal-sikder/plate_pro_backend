from rest_framework import serializers #type: ignore
from ..models import PlateShape

class PlateShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlateShape
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
