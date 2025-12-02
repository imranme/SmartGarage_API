from django.urls import path
from . import views
urlpatterns = [
    path('vehicles/', views.VehicleListCreateAPIView.as_view(), name='vehicle-list-create'),
    path('vehicles/vehicle-details/<uuid:uid>/', views.VehicleRetrieveUpdateDestroyAPIView.as_view(), name='vehicle-detail'),
    path('locations/', views.LocationListCreateAPIView.as_view(), name='location-list-create'),
    path('locations/<uuid:uid>/', views.LocationRetrieveUpdateDestroyAPIView.as_view(),name='location-detail'),
]