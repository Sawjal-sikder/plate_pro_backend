from rest_framework import serializers #type: ignore
from ..models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    plate_variant_price = serializers.SerializerMethodField()
    drilling_service_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ["id", "plate_variant", "quantity", "plate_variant_price", "drilling_service", "holes_count", "drilling_service_price", "total_price", "created_at", "updated_at"]
        read_only_fields = ["id", "plate_variant_price", "drilling_service_price", "total_price", "created_at", "updated_at"]
    
    def get_plate_variant_price(self, instance):
        if instance.plate_variant:
            return float(instance.plate_variant.price) * int(instance.quantity)
        return 0
    
    def get_drilling_service_price(self, instance):
        if instance.drilling_service and instance.holes_count:
            return float(instance.drilling_service.price_per_hole) * int(instance.holes_count)
        return 0
    
    def get_total_price(self, instance):
        return self.get_plate_variant_price(instance) + self.get_drilling_service_price(instance)
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.plate_variant:
            representation["plate_variant"] = {
                "id": instance.plate_variant.id,
                "name": instance.plate_variant.name,
                "price": instance.plate_variant.price
            }
        else:
            representation["plate_variant"] = None
        
        if instance.drilling_service:
            representation["drilling_service"] = {
                "id": instance.drilling_service.id,
                "name": instance.drilling_service.name,
                "price_per_hole": instance.drilling_service.price_per_hole
            }
        else:
            representation["drilling_service"] = None
            
        return representation