from rest_framework import serializers #type: ignore
from services.models import Order, OrderItem, PlateVariant, DrillingService, CartItem

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "plate_variant",
            "drilling_service",
            "quantity",
            "holes_count",
            "price",
        ]
        read_only_fields = ["id", "price"]
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['plate_variant'] = {
            "plate_variant_id": instance.plate_variant.id,
            "name": instance.plate_variant.name,
            "price": instance.plate_variant.price
        } if instance.plate_variant else None
        
        representation['drilling_service'] = {
            "drilling_service_id": instance.drilling_service.id,
            "name": instance.drilling_service.name,
            "price_per_hole": instance.drilling_service.price_per_hole
        } if instance.drilling_service else None
        return representation


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    # Input fields for single item
    plate_variant = serializers.PrimaryKeyRelatedField(
        queryset=PlateVariant.objects.all(), write_only=True
    )
    drilling_service = serializers.PrimaryKeyRelatedField(
        queryset=DrillingService.objects.all(), write_only=True, required=False, allow_null=True
    )
    quantity = serializers.IntegerField(write_only=True, min_value=1, default=1)
    holes_count = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "total_amount",
            "status",
            "items",
            "created_at",
            "updated_at",
            "plate_variant",
            "drilling_service",
            "quantity",
            "holes_count",
        ]
        read_only_fields = ["created_at", "updated_at", "total_amount", "status", "id", "user"]
        
    def create(self, validated_data):
        from decimal import Decimal
        
        # Extract single item fields
        plate_variant = validated_data.pop("plate_variant")
        drilling_service = validated_data.pop("drilling_service", None)
        quantity = validated_data.pop("quantity", 1)
        holes_count = validated_data.pop("holes_count", None)
        
        # Calculate item price
        item_price = Decimal("0.00")
        
        # Calculate price for plate variant
        if plate_variant:
            item_price += plate_variant.price * quantity
        
        # Calculate price for drilling service
        if drilling_service and holes_count:
            item_price += drilling_service.price_per_hole * holes_count
        
        total_amount = item_price
        
        # Create order with calculated total
        order = Order.objects.create(total_amount=total_amount, **validated_data)

        # Create order item
        OrderItem.objects.create(
            order=order,
            plate_variant=plate_variant,
            drilling_service=drilling_service,
            quantity=quantity,
            holes_count=holes_count,
            price=item_price
        )

        # Delete all cart items for the current user
        user = validated_data.get('user') or order.user
        CartItem.objects.filter(user=user).delete()

        return order
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = OrderItemSerializer(instance.items.all(), many=True).data
        return representation

