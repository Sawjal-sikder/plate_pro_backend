from rest_framework import serializers


class CornerSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    radius = serializers.FloatField()


class HoleSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    radius = serializers.FloatField()


class BoundingBoxSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()
    width = serializers.FloatField()
    height = serializers.FloatField()


class PlateDataSerializer(serializers.Serializer):
    viewBox = serializers.CharField(max_length=100)
    boundingBox = BoundingBoxSerializer()
    corners = CornerSerializer(many=True)
    holes = HoleSerializer(many=True, required=False)
    svgPath = serializers.CharField(max_length=5000)
    color = serializers.CharField(max_length=20)
