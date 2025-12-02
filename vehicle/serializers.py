from rest_framework import serializers
from .models import Vehicle, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['uid', 'store_name', 'address', 'created_at', 'updated_at']
        read_only_fields = ['uid', 'created_at', 'updated_at']


class VehicleSerializer(serializers.ModelSerializer):
    store_of_purchase = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Vehicle
        fields = ['uid', 'vin', 'brand', 'model', 'year', 'date_of_purchase', 'store_of_purchase', 'location_id', 'image', 'created_at', 'updated_at']
        read_only_fields = ['uid', 'created_at', 'updated_at']

    def create(self, validated_data):
        store_of_purchase = validated_data.pop('store_of_purchase', None)
        vehicle = Vehicle.objects.create(**validated_data)
        if store_of_purchase is not None:
            vehicle.store_of_purchase = store_of_purchase
            vehicle.save()
        return vehicle
    
    def update(self, instance, validated_data):
        location = validated_data.pop('location', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if location is not None:
            instance.location = location
        instance.save()
        return instance
    