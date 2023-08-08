from django.db import models
from base.models import User
from cars.models import Car, CarSlot
# Create your models here.

class Order(models.Model):
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_product

class CarBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    slot = models.ForeignKey(CarSlot, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
        ('picked_up', 'Picked Up'),
        ('returned', 'Returned'),
        ('late', 'Late Return'),
        ('damage', 'Damage Reported'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_payment_id = models.CharField(max_length=100)
    booking_order_id = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now=True)

    late_return_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    damage_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_charges(self):
        total_charges = self.car.price_per_day * self.get_booking_duration()

        if self.late_return_charges:
            total_charges += self.late_return_charges

        if self.damage_charges:
            total_charges += self.damage_charges

        return total_charges

    def get_booking_duration(self):
        return 1

    def __str__(self):
        return f"{self.user.username} - {self.car.name} - {self.slot.date}"
    