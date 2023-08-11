from rest_framework import serializers
from base.serializers import UserSerializer
from cars.serializers import CarSerializer, CarSlotSerializer, LocationSerializer
from .models import CarBooking, Order


class CarBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    car = CarSerializer()
    slot = CarSlotSerializer()
    pickup_location = LocationSerializer()
    dropoff_location = LocationSerializer()

    class Meta:
        model = CarBooking
        fields = "__all__"


class CarBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBooking
        fields = ["status", "late_return_charges"]

    def validate(self, data):
        # Validate 'status' field
        status = data.get("status")
        if status == "late":
            # Ensure 'late_return_charges' is provided when status is 'late'
            late_return_charges = data.get("late_return_charges")
            if late_return_charges is None:
                raise serializers.ValidationError(
                    "Late charges are required when status is 'late'"
                )
            # You can perform additional validation on 'late_return_charges' if needed

        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
