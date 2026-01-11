from django.urls import path #type: ignore
from .views import plate_calculate_views, plate_shape

urlpatterns = [
    path('calculate/', plate_calculate_views.PlateCalculationView.as_view(), name='plate-calculate'),
    path('plate-shapes/list/', plate_shape.PlateShapeListView.as_view(), name='plate-shape-list'),
    path('plate-shapes/details/<int:pk>/', plate_shape.PlateShapeRetriveView.as_view(), name='plate-shape-detail'),
    # for dashboard
    path('plate-shapes/', plate_shape.PlateShapeListCreateView.as_view(), name='plate-shape-list-create'),
    path('plate-shapes/<int:pk>/', plate_shape.PlateShapeRetrieveUpdateDestroyView.as_view(), name='plate-shape-detail-dashboard'),
]
