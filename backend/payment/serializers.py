from rest_framework import serializers
from base.serializers import UserSerializer
from cars.serializers import CarSerializer, CarSlotSerializer
from .models import CarBooking

class CarBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    car = CarSerializer()
    slot = CarSlotSerializer()

    class Meta:
        model = CarBooking
        fields = '__all__'