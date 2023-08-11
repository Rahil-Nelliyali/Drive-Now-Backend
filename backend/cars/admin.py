from django.contrib import admin
from .models import Car, CarCategory, CarSlot, Location

admin.site.register(Car)
admin.site.register(CarCategory)
admin.site.register(CarSlot)
admin.site.register(Location)
