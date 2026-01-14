# from rest_framework import generics, permissions #type: ignore
# from ..models import CartItem
# from ..serializers.cart_item import CartItemSerializer

# class CartItemListCreateView(generics.ListCreateAPIView):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)