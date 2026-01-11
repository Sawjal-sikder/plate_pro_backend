from rest_framework import serializers #type: ignore
from ..models import PlateShape,  PlateVariant


class PlateVariantSerializer(serializers.ModelSerializer):  
    class Meta:
        model = PlateVariant
        fields = ["id", "name", "price", "plate_shape", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['plate_shape'] = {
            "id": instance.plate_shape.id,
            "name": instance.plate_shape.name
        }
        return representation

class PlateShapeSerializer(serializers.ModelSerializer):
    variants = PlateVariantSerializer(many=True, read_only=True)

    class Meta:
        model = PlateShape
        fields = ["id", "name", "icon", "description", "points", "variants" , "closed", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
