from rest_framework import generics, permissions, response #type: ignore
from services.serializers.DrillingArea import DrillingAreaSerializer
from services.models import DrillingArea

class DrillingAreaView(generics.RetrieveUpdateAPIView):
    queryset = DrillingArea.objects.all()
    serializer_class = DrillingAreaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        # Always return the first DrillingArea instance, or create one if it doesn't exist
        obj, created = DrillingArea.objects.get_or_create(id=1)
        return obj
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response({
            "message": "Drilling area updated successfully",
            "data": serializer.data
        })