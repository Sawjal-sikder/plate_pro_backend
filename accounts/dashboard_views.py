from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()
from services.models import Order, PlateShape, PlateVariant

from rest_framework.views import APIView #type: ignore
from rest_framework.response import Response #type: ignore
from rest_framework import permissions, status #type: ignore

class DashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        data = {
            'current_user': request.user.full_name,
            'total_users': User.objects.count(),
            'total_plate_shapes': PlateShape.objects.count(),
            'total_plate_variants': PlateVariant.objects.count(),
            'total_orders': Order.objects.count(),
        }
        return Response(data, status=status.HTTP_200_OK)