from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Service, SellVehicle
from apps.vehicle.models import Vehicle, Location

User = get_user_model()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('uid', 'store_name', 'address', 'created_at', 'updated_at')
        read_only_fields = ('uid', 'created_at', 'updated_at')


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('uid', 'vin', 'brand', 'model', 'year', 'date_of_purchase')
        read_only_fields = ('uid',)


class ServiceListSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ('uid', 'vehicle', 'location', 'appointment_date', 'serviced_before', 'cancelled', 'created_at', 'updated_at')
        read_only_fields = ('uid', 'cancelled', 'created_at', 'updated_at')


class ServiceDetailSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ('uid', 'vehicle', 'location', 'description', 'appointment_date', 'serviced_before', 'cancelled', 'created_at', 'updated_at')
        read_only_fields = ('uid', 'cancelled', 'created_at', 'updated_at')


class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
    vehicle = serializers.CharField()
    location = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Service
        fields = ('vehicle', 'location', 'description', 'appointment_date', 'serviced_before')

    def validate_vehicle(self, value):
        try:
            vehicle = Vehicle.objects.get(uid=value)
            return vehicle
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError("Vehicle not found.")

    def validate_location(self, value):
        if value:
            try:
                location = Location.objects.get(uid=value)
                return location
            except Location.DoesNotExist:
                raise serializers.ValidationError("Location not found.")
        return None

    def validate(self, data):
        request = self.context.get('request')
        vehicle = data.get('vehicle')

        # Ensure vehicle belongs to the user
        if vehicle and vehicle.user != request.user:
            raise serializers.ValidationError("You can only create services for your own vehicles.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Service.objects.create(**validated_data)


class ServiceCancelSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        instance.cancelled = True
        instance.save()
        return instance


class SellVehicleListSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = SellVehicle
        fields = ('uid', 'vehicle', 'user', 'requested_at')
        read_only_fields = ('uid', 'requested_at')

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'phone_number': obj.user.phone_number
        }


class SellVehicleCreateSerializer(serializers.ModelSerializer):
    vehicle = serializers.CharField()

    class Meta:
        model = SellVehicle
        fields = ('vehicle',)

    def validate_vehicle(self, value):
        try:
            vehicle = Vehicle.objects.get(uid=value)
            return vehicle
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError("Vehicle not found.")

    def validate(self, data):
        request = self.context.get('request')
        vehicle = data.get('vehicle')

        # Ensure vehicle belongs to the user
        if vehicle and vehicle.user != request.user:
            msg = 'You can only create sell requests for your own vehicles.'
            raise serializers.ValidationError(msg)

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return SellVehicle.objects.create(**validated_data)
    


