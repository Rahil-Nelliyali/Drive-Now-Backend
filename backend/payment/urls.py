from django.urls import path
from . import views


urlpatterns = [
    path('pay/',views.Start_payment.as_view(), name="payment"),
    path('success/',views.Handle_payment_success.as_view(), name="payment_success"),
    path('bookings/',views.BookingListView.as_view(),name="bookings"),

    #renter side
    
    path('renterbookings/<int:id>/',views. RenterBookingsAPIView.as_view(), name='renter_bookings'),
    path('updatebooking/<int:appointment_id>/',views.Update_booking, name='update_booking'),

]