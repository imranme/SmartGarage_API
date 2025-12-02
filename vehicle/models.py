from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Current User model
User = get_user_model()


def vehicle_image_upload_path(instance, filename):
    """Vehicle image path generator"""
    user_email = instance.user.email.replace("@", "_")
    return f"vehicles/{instance.vin}/{filename}"


class Location(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    store_name = models.CharField(max_length=255)  
    address = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.store_name} - {self.address}"


class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    vin = models.CharField(max_length=100)
    brand = models.CharField(max_length=155)
    model = models.CharField(max_length=155)
    year = models.IntegerField()
    date_of_purchase = models.DateField()
    store_of_purchase = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=vehicle_image_upload_path, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return f"{self.vin} - {self.brand} {self.model}"
