# from django.db import models
# # from vehicle.models import Vehicle 
# # from user.models import user
# # from vehicle.models import Location
# import uuid

# class Service(models.Model):
#     # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
#     # vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='services')
#     uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
#     description = models.TextField(blank=True, null=True)
#     location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
#     appointment_date = models.DateTimeField()
#     serviced_before = models.BooleanField(default=False)
#     cancelled = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Service"
#         verbose_name_plural = "Services"

#     def __str__(self):
#         return f'Service {self.uid} for Vehicle {self.vehicle.vin}-{self.vehicle.brand} {self.vehicle.model}-{self.user.email}'
    
# class SellVehicle(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sell_vehicle_requests')
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='sell_requests')
#     uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
#     requested_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Sell Vehicle"
#         verbose_name_plural = "Sell Vehicles"
#     def __str__(self):
#         return f'Sell Request {self.uid} for Vehicle {self.vehicle.vin}-{self.vehicle.brand} {self.vehicle.model}-{self.user.email}'