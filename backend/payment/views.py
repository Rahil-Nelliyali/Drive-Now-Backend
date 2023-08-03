from django.shortcuts import render
from rest_framework.views import APIView
from base.models import User, Renter
from cars.models import Car, CarSlot
import razorpay
from datetime import datetime
from .serializers import CarBookingSerializer, CarSerializer, CarSlotSerializer
from rest_framework.response import Response
import json
from .models import CarBooking
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view



class Start_payment(APIView):
    def post(self, request, format=None):
        try:
            amount = request.data['amount']
            amount_in_paise = int(float(amount) * 100)

            current_user = request.data['user']
            user = User.objects.get(id=current_user)

            car = request.data['car']
            car = Car.objects.get(id=car)

            slot = request.data['slot']
            current_slot = CarSlot.objects.get(id=slot)

            PUBLIC_KEY = 'rzp_test_t7mDyb37sLmED8'
            SECRET_KEY = '4YMuQlfTvyvuyHgdtpyoxkDW'

            # setup razorpay client this is the client to whome user is paying money that's you
            client = razorpay.Client(auth=(PUBLIC_KEY,SECRET_KEY))


            payment = client.order.create({"amount": amount_in_paise, 
                                        "currency": "INR", 
                                        "payment_capture": "1"})
            
            
        

            order = CarBooking.objects.create(
                                        user = user,
                                        booking_payment_id = payment['id'],
                                        booking_date = datetime.now().date(),
                                        car = car,
                                        slot = current_slot,
                                    )

            serializer = CarBookingSerializer(order)
        
            data = {
                "payment": payment,
                "order": serializer.data
            }
            return Response(data)
        except Exception as e:
            # Log the error for debugging purposes
            print("Error occurred during payment:", str(e))
            # Return a custom error response
            return Response({"error": "An error occurred during payment processing."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Handle_payment_success(APIView):
    def post(self, request, format=None):
        res = json.loads(request.data["response"])
        slot = request.data['slot']
       


        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        # res.keys() will give us list of keys in res
        for key in res.keys():
            if key == 'razorpay_order_id':
                ord_id = res[key]
            elif key == 'razorpay_payment_id':
                raz_pay_id = res[key]
            elif key == 'razorpay_signature':
                raz_signature = res[key]

        order = CarBooking.objects.get(appointment_payment_id=ord_id)

        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }

        PUBLIC_KEY = 'rzp_test_t7mDyb37sLmED8'
        SECRET_KEY = '4YMuQlfTvyvuyHgdtpyoxkDW'

        client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))

        check = client.utility.verify_payment_signature(data)


        order.isPaid = True
        order.save()
        slot = CarSlot.objects.get(id=slot)
        slot.is_booked = True
        slot.save()
    
     
        res_data = {
            'message': 'payment successfully received!',
            'order_id' : ord_id
        }

        return Response(res_data)
    


class BookingListView(ListAPIView):
    serializer_class = CarBookingSerializer
    def get_queryset(self):
        return CarBooking.objects.all()


class RenterBookingsAPIView(APIView):
    def get(self, request,id):
        try:
            current_user=User.objects.get(id=id)
            car = Car.objects.get(user=current_user)
            bookings = CarBooking.objects.filter(car=car)
            serializer = CarBookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CarBooking.DoesNotExist:
            return Response("Bookings not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def Update_booking(request, booking_id):
    try:
        booking = CarBooking.objects.get(id=booking_id)
    except CarBooking.DoesNotExist:
        return Response({"message": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    if not new_status:
        return Response({"message": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)

    booking.status = new_status
    booking.save()

    return Response({"message": "Booking status updated successfully"})
