from rest_framework import serializers
from base.serializers import UserSerializer
from cars.serializers import CarSerializer, CarSlotSerializer
from .models import CarBooking, Order

class CarBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    car = CarSerializer()
    slot = CarSlotSerializer()

    class Meta:
        model = CarBooking
        fields = '__all__'

class CarBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBooking
        fields = ['status']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'