from rest_framework import generics, permissions, response #type: ignore
from rest_framework.views import APIView #type: ignore
from services.mail_orderpdf import send_order_html_email
from services.models import OrderPlate, OrderItemPlate
from services.serializers.plate_order_serializer import OrderItemPlateSerializer, OrderPlateCreateWithItemsSerializer, OrderPlateSerializer



class CreateOrderPlateView(generics.CreateAPIView):
    queryset = OrderPlate.objects.all()
    serializer_class = OrderPlateCreateWithItemsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderPlateListView(generics.ListAPIView):
    queryset = OrderPlate.objects.all()
    serializer_class = OrderPlateSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    
    
    
class OrderPlateSendMailView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.query_params.get('order_id')
        email = request.query_params.get('email')
        
        if not order_id or not email:
            return response.Response({'message': 'Order ID and email are required.'}, status=400)
        
        try:
            order = OrderPlate.objects.get(id=order_id, user=request.user)
            serializer = OrderPlateSerializer(order)
            order_data = serializer.data
            send_order_html_email.delay(order_data, email)
            
            return response.Response({'message': 'Order details sent via email successfully.', 'data': order_data}, status=200)
        except OrderPlate.DoesNotExist:
            return response.Response({'message': 'Order not found.'}, status=404)