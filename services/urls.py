from django.urls import path #type: ignore
from .views import plate_calculate_views, plate_shape, plate_shape_variant, cart_item

urlpatterns = [
    path('calculate/', plate_calculate_views.PlateCalculationView.as_view(), name='plate-calculate'),
    path('plate-shapes/list/', plate_shape.PlateShapeListView.as_view(), name='plate-shape-list'),
    path('plate-shapes/details/<int:pk>/', plate_shape.PlateShapeRetriveView.as_view(), name='plate-shape-detail'),
    # cart item URLs
    path('cart-items/', cart_item.CartItemListCreateView.as_view(), name='cart-item-list-create'),
    
    
    # for dashboard
    path('plate-shapes/', plate_shape.PlateShapeListCreateView.as_view(), name='plate-shape-list-create'),
    path('plate-shapes/<int:pk>/', plate_shape.PlateShapeRetrieveUpdateDestroyView.as_view(), name='plate-shape-detail-dashboard'),
    # PlateVariant URLs
    path('plate-variants/', plate_shape_variant.PlateShapeVariantListCreateView.as_view(), name='plate-variant-list-create'),
    path('plate-variants/<int:pk>/', plate_shape_variant.PlateShapeVariantRetrieveUpdateDestroyView.as_view(), name='plate-variant-detail-dashboard'),
    # DrillingService URLs
]
