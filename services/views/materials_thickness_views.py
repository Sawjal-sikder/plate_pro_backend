from rest_framework import generics, permissions, response, status #type: ignore
from services.models import Materials, Thickness
from services.serializers.materials_thickness_serializer import MaterialsSerializer, ThicknessSerializer


class MaterialsListCreateView(generics.ListCreateAPIView):
    queryset = Materials.objects.all()
    serializer_class = MaterialsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        materials = self.get_queryset()
        serializer = self.get_serializer(materials, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ThicknessListCreateView(generics.ListCreateAPIView):
    queryset = Thickness.objects.all()
    serializer_class = ThicknessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        thicknesses = self.get_queryset()
        serializer = self.get_serializer(thicknesses, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)