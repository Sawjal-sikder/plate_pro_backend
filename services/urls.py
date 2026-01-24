from django.urls import path #type: ignore
from .views import (
    plate_shape,
    plate_shape_variant,
    drilling_service,
    add_to_cart,
    order_view,
)
from .views.materials_thickness_views import (
    MaterialsListCreateView,
    ThicknessListCreateView,
)

from .views.plate_order_views import (
    CreateOrderPlateView,
    OrderPlateListCreateView,
    OrderPlateDetailView,
    OrderItemPlateListCreateView,
    OrderItemPlateDetailView,

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
    
    
    # Materials and Thickness URLs
    path('materials/', MaterialsListCreateView.as_view(), name='materials-list-create'),
    # path('materials/<int:pk>/', MaterialsRetrieveUpdateDestroyView.as_view(), name='materials-detail-dashboard'),
    path('thicknesses/', ThicknessListCreateView.as_view(), name='thickness-list-create'),
    # path('thicknesses/<int:pk>/', ThicknessRetrieveUpdateDestroyView.as_view(), name='thickness-detail-dashboard'),
    
    
    # Plate Order URLs
    path('order-plates/create/', CreateOrderPlateView.as_view(), name='create-order-plate'),
    path('order-plates/', OrderPlateListCreateView.as_view(), name='order-plate-list-create'),
    path('order-plates/<int:pk>/', OrderPlateDetailView.as_view(), name='order-plate-detail'),
    path('order-plates/items/', OrderItemPlateListCreateView.as_view(), name='order-item-plate-list-create'),
    path('order-plates/items/<int:pk>/', OrderItemPlateDetailView.as_view(), name='order-item-plate-detail'),
    
]
