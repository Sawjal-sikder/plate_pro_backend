from django.urls import path
from .views import PlateCalculationView, DownloadDXFView

urlpatterns = [
    path('calculate/', PlateCalculationView.as_view(), name='plate-calculate'),
    path('download-dxf/', DownloadDXFView.as_view(), name='download-dxf'),
]
