from django.urls import path #type: ignore
from .views import (
    plate_shape,
    plate_shape_variant,
    drilling_service,
    add_to_cart,
    order_view,
)

urlpatterns = [
    path('plate-shapes/list/', plate_shape.PlateShapeListView.as_view(), name='plate-shape-list'),
    path('plate-shapes/details/<int:pk>/', plate_shape.PlateShapeRetriveView.as_view(), name='plate-shape-detail'),
    # cart item URLs
    # path('cart-items/', cart_item.CartItemListCreateView.as_view(), name='cart-item-list-create'),
    path("cart/", add_to_cart.AddToCartView.as_view(), name="add-to-cart"),
    path("orders/", order_view.OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", order_view.OrderDetailView.as_view(), name="order-detail"),
    
    
    # for dashboard
    path('plate-shapes/', plate_shape.PlateShapeListCreateView.as_view(), name='plate-shape-list-create'),
    path('plate-shapes/<int:pk>/', plate_shape.PlateShapeRetrieveUpdateDestroyView.as_view(), name='plate-shape-detail-dashboard'),
    # PlateVariant URLs
    path('plate-variants/', plate_shape_variant.PlateShapeVariantListCreateView.as_view(), name='plate-variant-list-create'),
    path('plate-variants/<int:pk>/', plate_shape_variant.PlateShapeVariantRetrieveUpdateDestroyView.as_view(), name='plate-variant-detail-dashboard'),
    # DrillingService URLs
    path('drilling-services/', drilling_service.DrillingServiceCreateListView.as_view(), name='drilling-service-list-create'),
    path('drilling-services/<int:pk>/', drilling_service.DrillingServiceRetrieveUpdateDestroyView.as_view(), name='drilling-service-detail-dashboard'),
]
