from rest_framework import generics, permissions, response #type: ignore

from ..serializers.drilling_service import DrillingServiceSerializer
from ..models import DrillingService

class DrillingServiceCreateListView(generics.ListCreateAPIView):
    queryset = DrillingService.objects.all()
    serializer_class = DrillingServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        self.perform_create(serializers)
        return response.Response({
            "message": "Drilling service created successfully",
            "data": serializers.data
        })
        

class DrillingServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DrillingService.objects.all()
    serializer_class = DrillingServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response({
            "message": "Drilling service updated successfully",
            "data": serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response({
            "message": "Drilling service deleted successfully"
        })