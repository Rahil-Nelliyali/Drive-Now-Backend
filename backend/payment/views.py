from django.shortcuts import render
from rest_framework.views import APIView
from base.models import User, Renter
from cars.models import Car, CarSlot, Location
import razorpay
from datetime import datetime
from .serializers import (
    CarBookingUpdateSerializer,
    CarBookingSerializer,
    OrderSerializer,
)
from rest_framework.response import Response
import json
from .models import CarBooking, Order
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from decimal import Decimal
from .signals import order_paid_signal, booking_updated_signal
from django.core.mail import send_mail


class Start_payment(APIView):
    def post(self, request, format=None):
        try:
            amount = request.data["amount"]
            amount_in_paise = int(float(amount) * 100)

            current_user = request.data["user"]
            user = User.objects.get(id=current_user)

            car = request.data["car"]
            car = Car.objects.get(id=car)

            slot = request.data["slot"]
            current_slot = CarSlot.objects.get(id=slot)

            pickup_location_id = request.data["pickup_location"]
            pickup_location = Location.objects.get(id=pickup_location_id)

            dropoff_location_id = request.data["dropoff_location"]
            dropoff_location = Location.objects.get(id=dropoff_location_id)

            PUBLIC_KEY = "rzp_test_t7mDyb37sLmED8"
            SECRET_KEY = "4YMuQlfTvyvuyHgdtpyoxkDW"

            # setup razorpay client
            client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))

            payment = client.order.create(
                {"amount": amount_in_paise, "currency": "INR", "payment_capture": "1"}
            )

            order_id = payment["id"]  # Corrected line to access payment id as order_id

            print("Order ID:", order_id)

            order = CarBooking.objects.create(
                user=user,
                booking_order_id=order_id,
                booking_date=datetime.now().date(),
                car=car,
                slot=current_slot,
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
            )

            serializer = CarBookingSerializer(order)

            data = {"payment": payment, "order": serializer.data}
            return Response(data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Car.DoesNotExist:
            return Response(
                {"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except CarSlot.DoesNotExist:
            return Response(
                {"error": "Car slot not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            # Log the error for debugging purposes
            print("Error occurred during payment:", str(e))
            # Return a custom error response to the user
            return Response(
                {"error": "An unexpected error occurred. Please contact support."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Handle_payment_success(APIView):
    def post(self, request, format=None):
        res = json.loads(request.data["response"])
        slot = request.data["slot"]

        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        # res.keys() will give us list of keys in res
        for key in res.keys():
            if key == "razorpay_order_id":
                ord_id = res[key]
            elif key == "razorpay_payment_id":
                raz_pay_id = res[key]
            elif key == "razorpay_signature":
                raz_signature = res[key]

        raz_pay_id = res.get("razorpay_payment_id")
        payment_id = raz_pay_id
        try:
            order = CarBooking.objects.get(booking_order_id=ord_id)
        except CarBooking.DoesNotExist:
            return Response(
                {"error": "Payment details not found or already processed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print("orderid: ", ord_id)
        print("paymentid: ", payment_id)
        data = {
            "razorpay_order_id": ord_id,
            "razorpay_payment_id": raz_pay_id,
            "razorpay_signature": raz_signature,
        }

        PUBLIC_KEY = "rzp_test_t7mDyb37sLmED8"
        SECRET_KEY = "4YMuQlfTvyvuyHgdtpyoxkDW"

        client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))

        check = client.utility.verify_payment_signature(data)
        order.booking_payment_id = payment_id
        order.is_paid = True
        order.save()
        slot = CarSlot.objects.get(id=slot)
        slot.is_booked = True
        slot.save()

        # Sending email notifications using signals
        order_paid_signal.send(sender=self.__class__, order=order)

        res_data = {"message": "payment successfully received!", "order_id": ord_id}

        return Response(res_data)


from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView


class BookingListView(RetrieveAPIView):
    queryset = CarBooking.objects.all()
    serializer_class = CarBookingSerializer
    lookup_field = "user_id"


class RenterBookingsAPIView(APIView):
    def get(self, request, id):
        try:
            current_user = User.objects.get(id=id)
            car = Car.objects.get(user=current_user)
            bookings = CarBooking.objects.filter(car=car)
            serializer = CarBookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CarBooking.DoesNotExist:
            return Response("Bookings not found", status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def Update_booking(request, booking_id):
    try:
        booking = CarBooking.objects.get(id=booking_id)
    except CarBooking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

    serializer = CarBookingUpdateSerializer(booking, data=request.data)
    if serializer.is_valid():
        if serializer.validated_data.get("status") == "late":
            late_return_charges = serializer.validated_data.get("late_return_charges")
            if late_return_charges is not None:
                booking.late_return_charges = late_return_charges
        elif serializer.validated_data.get("status") in ["rejected", "cancelled"]:
            # Initiate refund using Razorpay API
            PUBLIC_KEY = "rzp_test_t7mDyb37sLmED8"
            SECRET_KEY = "4YMuQlfTvyvuyHgdtpyoxkDW"
            # Convert Decimal to float before creating the refund data
            refund_amount = float(booking.car.price_per_day) * 100

            client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))
            # Fetch payment details using the order ID

            # Retrieve payment ID from payment details
            payment_id = booking.booking_payment_id
            print(payment_id)
            refund_data = {
                "payment_id": payment_id,
                "amount": refund_amount,
                "notes": {"reason": "User cancelled order"},
            }
            refund = client.refund.create(data=refund_data)
            booking.status = "cancelled"
            booking.is_paid = False
        serializer.save()
        booking_updated_signal.send(sender=Update_booking, booking=booking)

        return Response(serializer.data, status=200)
    else:
        return Response(serializer.errors, status=400)


from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist


@api_view(["PUT"])
def cancel_booking(request, booking_id):
    try:
        booking = CarBooking.objects.get(id=booking_id)
    except ObjectDoesNotExist:
        return Response(
            {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        booking.slot.is_booked = False
        booking.slot.save()

        serializer = CarBookingUpdateSerializer(booking, data=request.data)
        serializer.is_valid(raise_exception=True)

        if booking.status == "cancelled":
            return Response(
                {"error": "Booking is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refund_amount = float(booking.car.price_per_day) * 100

        client = razorpay.Client(auth=("YOUR_PUBLIC_KEY", "YOUR_SECRET_KEY"))

        refund_data = {
            "payment_id": booking.booking_payment_id,
            "amount": refund_amount,
            "notes": {"reason": "User cancelled order"},
        }
        refund = client.refund.create(data=refund_data)

        booking.status = "cancelled"
        booking.is_paid = False
        booking.save()
        refund = client.refund.fetch(refund["id"])
        booking_updated_signal.send(sender=cancel_booking, booking=booking)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CarBooking
from .serializers import CarBookingSerializer


@api_view(["GET"])
def get_user_bookings(request):
    user_id = request.query_params.get("user")

    bookings = CarBooking.objects.filter(user__id=user_id)

    serializer = CarBookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_renter_bookings(request):
    user_id = request.query_params.get("user")
    cars_added_by_renter = Car.objects.filter(renter_id=user_id)

    bookings = CarBooking.objects.filter(car__in=cars_added_by_renter)
    serializer = CarBookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_bookings(request):
    bookings = CarBooking.objects.all()
    serializer = CarBookingSerializer(bookings, many=True)
    return Response(serializer.data)


from rest_framework import status


@api_view(["GET"])
def get_bookings_for_car(request, car_id):
    try:
        bookings = CarBooking.objects.filter(car_id=car_id)
        if not bookings:
            return Response(
                {"message": "No bookings found for this car."},
                status=status.HTTP_204_NO_CONTENT,
            )

        serializer = CarBookingSerializer(bookings, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.dispatch import receiver
from .signals import order_paid_signal, booking_updated_signal
from django.core.mail import send_mail
from django.conf import settings

from django.urls import reverse


@receiver(order_paid_signal)
def send_order_paid_notification(sender, order, **kwargs):
    user_redirect = "https://drive-now-client.vercel.app/mybookings"
    user_subject = "Order Processing"
    user_message = f'Dear valued customer,\n\nWe greatly appreciate your recent order. Your order has been successfully received and is currently being processed. Kindly await confirmation of your order shortly.\n\nFor your convenience, you can track and manage all your bookings by visiting the following link: <a href="{user_redirect}">Booking Management Portal</a>.\n\nShould you require any assistance or have inquiries, please do not hesitate to contact our dedicated customer service team. We are here to provide the utmost support.\n\nThank you for choosing DriveNow.\n\nBest regards,\nTeam DriveNow'
    user_recipient_list = [order.user.email]

    renter_redirect = "https://drive-now-client.vercel.app/renterbookings"
    renter_subject = "New Order Received"
    renter_message = f'Dear esteemed partner,\n\nWe are pleased to inform you that a new order has been recieved. Your attention is kindly requested to review and confirm the details of this order at your earliest convenience.\n\nTo facilitate the management of your bookings, please access the following link: <a href="{renter_redirect}">Booking Management Portal</a>.\n\nShould you require any further assistance or have inquiries, please do not hesitate to contact our dedicated support team. We are committed to ensuring a seamless partnership experience.\n\nThank you for choosing DriveNow as your trusted partner.\n\nSincerely,\nTeam DriveNow'
    renter_recipient_list = [order.car.renter.email]

    # Send messages to user and renter
    send_mail(
        user_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        user_recipient_list,
        html_message=user_message,
    )
    send_mail(
        renter_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        renter_recipient_list,
        html_message=renter_message,
    )


@receiver(booking_updated_signal)
def send_booking_updated_notification(sender, booking, **kwargs):
    user_redirect = "https://drive-now-client.vercel.app/mybookings"
    user_subject = "Booking Update"
    user_message = f'Dear valued customer,We are pleased to notify you that your car booking has been successfully updated. Your reservation for the vehicle named {booking.car.name} has been adjusted and confirmed as per your request. To conveniently access and review the latest details of your bookings, kindly click on the following link:<a href="{user_redirect}">here</a>. Should you require any further assistance or have inquiries, please do not hesitate to get in touch with our dedicated support team. We are committed to ensuring your experience with DriveNow is consistently exceptional. We appreciate your trust in DriveNow for your car rental needs and sincerely look forward to the opportunity to serve you again.Best regards,Team DriveNow'
    user_recipient_list = [booking.user.email]

    renter_redirect = "https://drive-now-client.vercel.app/renterbookings"
    renter_subject = "Booking Update"
    renter_message = f'Dear {booking.car.renter},\n\nWe wish to inform you that the booking with ID {booking.id} for the car "{booking.car.name}" associated with your account has been successfully updated. This update was requested by the user {booking.user.first_name}.\n\nTo conveniently manage and review your bookings, please access the following link: [Manage Your Bookings](<a href="{renter_redirect}">here</a>).\n\nIf you have any questions or require further assistance, please do not hesitate to contact our dedicated support team. We are committed to ensuring a seamless experience for you and our valued users.\n\nThank you for choosing DriveNow for your car rental services.\n\nBest regards,\nTeam DriveNow'
    renter_recipient_list = [booking.car.renter.email]

    # Send messages to user and renter
    send_mail(
        user_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        user_recipient_list,
        html_message=user_message,
    )
    send_mail(
        renter_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        renter_recipient_list,
        html_message=renter_message,
    )
