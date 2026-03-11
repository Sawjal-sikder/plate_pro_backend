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


class MaterialsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Materials.objects.all()
    serializer_class = MaterialsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        material = self.get_object()
        serializer = self.get_serializer(material)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        material = self.get_object()
        serializer = self.get_serializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({"message": "Material updated successfully"}, status=status.HTTP_200_OK)
        return response.Response({"message": "Failed to update material"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        material = self.get_object()
        material.delete()
        return response.Response({"message": "Material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


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
            return response.Response({"message": "Thickness created successfully"}, status=status.HTTP_201_CREATED)
        return response.Response({"message": "Failed to create thickness"}, status=status.HTTP_400_BAD_REQUEST)


class ThicknessRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thickness.objects.all()
    serializer_class = ThicknessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
