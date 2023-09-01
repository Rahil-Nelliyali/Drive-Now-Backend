from django.urls import path
from . import views


urlpatterns = [
    path("pay/", views.Start_payment.as_view(), name="payment"),
    path("success/", views.Handle_payment_success.as_view(), name="payment_success"),
    path("bookings/", views.get_user_bookings, name="bookings"),
    # renter side
    path("renterbookings/", views.get_renter_bookings, name="renter_bookings"),
    path(
        "updatebooking/<int:booking_id>/", views.Update_booking, name="update_booking"
    ),
    path(
        "cancelbooking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"
    ),
    # admin
    path("allbookings/", views.get_all_bookings, name="bookings"),
    path(
        "get-bookings-for-car/<int:car_id>/",
        views.get_bookings_for_car,
        name="bookings",
    ),
]
