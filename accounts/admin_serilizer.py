from rest_framework import serializers #type: ignore
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "phone_number",
            "is_active",
            "is_staff",
            'password',
        ]
        read_only_fields = ["id", "is_active", "is_staff"]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user