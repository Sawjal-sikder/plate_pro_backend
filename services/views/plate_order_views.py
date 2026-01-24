from rest_framework import generics, permissions, response #type: ignore
from services.models import OrderPlate, OrderItemPlate
from services.serializers.plate_order_serializer import OrderItemPlateSerializer, OrderPlateCreateWithItemsSerializer, OrderPlateSerializer



class CreateOrderPlateView(generics.CreateAPIView):
    queryset = OrderPlate.objects.all()
    serializer_class = OrderPlateCreateWithItemsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderPlateListCreateView(generics.ListCreateAPIView):
    queryset = OrderPlate.objects.all()
    serializer_class = OrderPlateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class OrderPlateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderPlate.objects.all()
    serializer_class = OrderPlateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    
    
    
    
    
    
    
class OrderItemPlateListCreateView(generics.ListCreateAPIView):
    queryset = OrderItemPlate.objects.all()
    serializer_class = OrderItemPlateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        if order_id:
            return self.queryset.filter(order__id=order_id, order__user=self.request.user)
        return self.queryset.filter(order__user=self.request.user)
        
        
class OrderItemPlateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItemPlate.objects.all()
    serializer_class = OrderItemPlateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        if order_id:
            return self.queryset.filter(order__id=order_id, order__user=self.request.user)
        return self.queryset.filter(order__user=self.request.user)
    