from django.contrib import admin
from .models import Car, CarCategory, CarSlot

admin.site.register(Car)
admin.site.register(CarCategory)
admin.site.register(CarSlot)
