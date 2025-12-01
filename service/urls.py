from django.urls import path
from .views import (
    ServiceListCreateView,
    ServiceDetailView,
    ServiceCancelView,
    SellVehicleListCreateView,
    SellVehicleDetailView
)

urlpatterns = [
    path('schedule-services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('schedule-services/<uuid:uid>/', ServiceDetailView.as_view(), name='service-detail'),
    path('schedule-services/<uuid:uid>/cancel/', ServiceCancelView.as_view(),
         name='service-cancel'),
    path('sell-vehicle/', SellVehicleListCreateView.as_view(),
         name='sell-vehicle-list-create'),
    path('sell-vehicle/<uuid:uid>/', SellVehicleDetailView.as_view(),
         name='sell-vehicle-detail'),
]
