from django.urls import path
from .views import PlateCalculationView

urlpatterns = [
    path('calculate/', PlateCalculationView.as_view(), name='plate-calculate'),
]
