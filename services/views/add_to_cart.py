from rest_framework import generics, permissions, status #type: ignore
from rest_framework.response import Response #type: ignore
from ..models import CartItem
from ..serializers.add_to_cart import CartItemSerializer, CartItemCreateSerializer

class AddToCartView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Item added to cart successfully',
            'cart_item': response.data
        }, status=status.HTTP_201_CREATED)