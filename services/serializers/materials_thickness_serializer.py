import json
from rest_framework import serializers #type: ignore
from services.models import Materials, Thickness

class ThicknessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thickness
        fields = ['id', 'materials', 'name', 'price', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class VariantInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thickness
        fields = ['id', 'name', 'price', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MaterialsSerializer(serializers.ModelSerializer):
    variants = VariantInlineSerializer(many=True, required=False)

    class Meta:
        model = Materials
        fields = ['id', 'name', 'icon', 'description', 'variants', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_internal_value(self, data):
        if hasattr(data, 'getlist'):
            mutable = data.copy()
            variants_raw = mutable.get('variants')
            if isinstance(variants_raw, str):
                try:
                    mutable.setlist('variants', [])
                    parsed = json.loads(variants_raw)
                    data = mutable
                    data._mutable = True
                except (json.JSONDecodeError, ValueError):
                    parsed = []
                ret = super().to_internal_value(data)
                variant_serializer = VariantInlineSerializer(data=parsed, many=True)
                variant_serializer.is_valid(raise_exception=True)
                ret['variants'] = variant_serializer.validated_data
                return ret
        return super().to_internal_value(data)

    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])
        material = Materials.objects.create(**validated_data)
        for variant in variants_data:
            Thickness.objects.create(materials=material, **variant)
        material.refresh_from_db()
        return material

    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if variants_data is not None:
            instance.variants.all().delete()
            for variant in variants_data:
                Thickness.objects.create(materials=instance, **variant)

        return instance