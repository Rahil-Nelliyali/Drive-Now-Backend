from rest_framework import serializers
from cars.models import Car, CarCategory

class CarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCategory
        fields = ['id', 'name', 'description', 'image']

class CarSerializer(serializers.ModelSerializer):
    category = CarCategorySerializer()  # Use the CarCategorySerializer to serialize the category field
    class Meta:
        model = Car
        fields = '__all__'
    

class PostCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
