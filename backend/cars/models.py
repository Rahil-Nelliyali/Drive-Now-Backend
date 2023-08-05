from django.db import models
from django.contrib.auth import get_user_model
from base.models import User



class CarCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='photos/car_categories')
    is_active = models.BooleanField(default=True)
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_categories')

    def __str__(self):
        return self.name
    

class Car(models.Model):
    name = models.CharField(max_length=500, null=False)
    brand = models.CharField(max_length=500, null=False)
    year_manufactured = models.PositiveIntegerField()
    mileage = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=100)
    transmission_type = models.CharField(max_length=100)
    seating_capacity = models.PositiveIntegerField()
    air_conditioned = models.BooleanField(default=False)
    power_windows = models.BooleanField(default=False)
    central_locking = models.BooleanField(default=False)
    audio_system = models.BooleanField(default=False)
    gps_navigation = models.BooleanField(default=False)
    description = models.CharField(max_length=600, null=False)
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/cars')
    is_active = models.BooleanField(default=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=True)
    is_rejected = models.BooleanField(default=False)
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')


    
    def __str__(self):
        return self.name
    
  
class CarSlot(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.car.name} - {self.date}"