from rest_framework.response import Response #type: ignore
from rest_framework import generics, permissions #type: ignore 

# Views for PlateShape model and serializer
from ..serializers.plate_shape import PlateShapeSerializer
from ..models import PlateShape


# for website
class PlateShapeListView(generics.ListAPIView):
    queryset = PlateShape.objects.all()
    serializer_class = PlateShapeSerializer
    permission_classes = [permissions.AllowAny] 
    
class PlateShapeRetriveView(generics.RetrieveAPIView):
    queryset = PlateShape.objects.all()
    serializer_class = PlateShapeSerializer
    permission_classes = [permissions.AllowAny]
    
    
#  for dashboard
class PlateShapeListCreateView(generics.ListCreateAPIView):
    queryset = PlateShape.objects.all()
    serializer_class = PlateShapeSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "Plate shape created successfully",
            "data": serializer.data
        })

class PlateShapeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlateShape.objects.all()
    serializer_class = PlateShapeSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "Plate shape updated successfully",
            "data": serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Plate shape deleted successfully"
        })
        
        
