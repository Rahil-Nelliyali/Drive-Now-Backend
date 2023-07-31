from django.contrib import admin
from .models import Renter


class RenterAdmin(admin.ModelAdmin):
    pass

admin.site.register(Renter,RenterAdmin)