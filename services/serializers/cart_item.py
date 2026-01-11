from rest_framework import serializers #type: ignore
from ..models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "item_type", "plate_variant", "quantity", "drilling_service", "holes_count", "total_price", "created_at", "updated_at"]
        read_only_fields = ["id", "total_price", "created_at", "updated_at"]
        
    def validate(self, data):
        item_type = data.get('item_type')
        
        if item_type == 'variant':
            if not data.get('plate_variant'):
                raise serializers.ValidationError({'message': 'This field is required for item_type "variant".'})
            
            data['drilling_service'] = None
            data['holes_count'] = None
            
        elif item_type == 'drilling':
            if not data.get('drilling_service'):
                raise serializers.ValidationError({'message': 'This field is required for item_type "drilling".'})
            if not data.get('holes_count'):
                raise serializers.ValidationError({'message': 'This field is required for item_type "drilling".'})
            
            data['plate_variant'] = None
            data['quantity'] = 1
        else:
            raise serializers.ValidationError({'message': 'Invalid item_type. Must be either "variant" or "drilling".'})
        
        return data
    
    def create(self, validated_data):
        item_type = validated_data.get('item_type')
        
        if item_type == 'variant':
            variant = validated_data.get('plate_variant')
            quantity = validated_data.get('quantity', 1)
            total_price = variant.price * quantity
        
        else:  # item_type == 'drilling'
            service = validated_data.get('drilling_service')
            holes_count = validated_data.get('holes_count', 0)
            total_price = service.price_per_hole * holes_count
            
        validated_data['total_price'] = total_price
        return CartItem.objects.create(**validated_data)