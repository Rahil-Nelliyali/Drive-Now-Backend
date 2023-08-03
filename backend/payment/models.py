from django.db import models
from base.models import User
from cars.models import Car, CarSlot
# Create your models here.

class CarBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    slot = models.ForeignKey(CarSlot, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('complete', 'Complete'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_payment_id = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.car.name} - {self.slot.start_time}"
