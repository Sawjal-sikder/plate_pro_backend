from rest_framework import serializers #type: ignore
from services.models import Materials, Thickness

class ThicknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thickness
        fields = ['id', 'materials', 'name', 'price', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MaterialsSerializer(serializers.ModelSerializer):
    variants = ThicknessSerializer(many=True, read_only=True)
    
    class Meta:
        model = Materials
        fields = ['id', 'name', 'icon', 'description', 'variants', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']