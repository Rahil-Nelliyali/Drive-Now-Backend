from rest_framework import serializers
from cars.models import Car, CarCategory, CarSlot, Location


class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class PostLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):
    renter_name = serializers.SerializerMethodField()
    renter_id = serializers.SerializerMethodField()

    category = CarCategorySerializer()

    class Meta:
        model = Car
        fields = "__all__"

    def get_renter_name(self, car):
        return car.renter.get_full_name()

    def get_renter_id(self, car):
        return car.renter.id


class PostCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class CarSlotSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = CarSlot
        fields = "__all__"


class PostCarSlotSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarSlot
        fields = "__all__"
