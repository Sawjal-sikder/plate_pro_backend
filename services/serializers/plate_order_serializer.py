from rest_framework import serializers #type: ignore
from services.models import OrderItemPlate, OrderPlate
from services.serializers.materials_thickness_serializer import MaterialsSerializer, ThicknessSerializer


class OrderItemPlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemPlate
        fields = '__all__'
        read_only_fields = ['created_at','updated_at']
        
        
class OrderPlateSerializer(serializers.ModelSerializer):
    plate_items = OrderItemPlateSerializer(many=True, read_only=True)
    material = MaterialsSerializer(read_only=True)
    thickness = ThicknessSerializer(read_only=True)
    
    class Meta:
        model = OrderPlate
        fields = ['id', 'user', 'tatalArea', 'totalPerimeter', 'material', 'thickness', 'color', 'totalDrilingHoles', 'total_price', 'plate_items', 'created_at', 'updated_at']
        read_only_fields = ['user','plate_items','created_at','updated_at']
        

class OrderPlateCreateWithItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPlate
        fields = ['id', 'user', 'tatalArea', 'totalPerimeter', 'material', 'thickness', 'color', 'totalDrilingHoles', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['user','created_at','updated_at']

   