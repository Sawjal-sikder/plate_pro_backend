from rest_framework import generics, permissions, filters, response #type: ignore
from .admin_serilizer import AdminUserSerializer
from django.contrib.auth import get_user_model #type: ignore
User = get_user_model()
from .pagination import UserPagination

class AdminView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'email', 'phone_number']
    pagination_class = UserPagination
    
    def get_queryset(self):
        return User.objects.filter(is_staff=True)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=True, is_staff=True)
        headers = self.get_success_headers(serializer.data)
        return response.Response({"message": "User created successfully", "data": serializer.data}, status=201, headers=headers)