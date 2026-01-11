from rest_framework.response import Response #type: ignore
from rest_framework import generics, permissions #type: ignore 

# Views for PlateShape model and serializer
from ..serializers.plate_shape import  PlateVariantSerializer
from ..models import  PlateVariant


class PlateShapeVariantListCreateView(generics.ListCreateAPIView):
    queryset = PlateVariant.objects.all()
    serializer_class = PlateVariantSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Plate variant created successfully",
            "data": serializer.data
        })
        
class PlateShapeVariantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlateVariant.objects.all()
    serializer_class = PlateVariantSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Plate variant updated successfully",
            "data": serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Plate variant deleted successfully"
        })