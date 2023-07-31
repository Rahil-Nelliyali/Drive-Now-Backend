from django.http import JsonResponse,HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from base.models import User
from rest_framework import generics 
from rest_framework import permissions
from .models import Renter
from rest_framework.decorators import api_view
from .serializers import RenterSerializer
from django.views.decorators.csrf import csrf_exempt

from .serializers import  RenterSerializer
from rest_framework import status



class RenterRegister(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        password = request.data.get('password')
        mobile_no = request.data.get('mobile_no')

        if not full_name or not email or not password or not mobile_no:
            return Response({'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if Renter.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists'}, status=status.HTTP_409_CONFLICT)

        if Renter.objects.filter(mobile_no=mobile_no).exists():
            return Response({'message': 'Phone number already exists'}, status=status.HTTP_409_CONFLICT)

        renter = Renter(full_name=full_name, email=email, password=password, mobile_no=mobile_no)
        renter.save()

        renter_id = renter.id
        return Response({'message': 'Renter registered successfully', 'renter_id': renter_id}, status=status.HTTP_201_CREATED)


class RenterList(generics.ListCreateAPIView):
   queryset = Renter.objects.all()
   serializer_class = RenterSerializer
   

    

class RenterDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset = Renter.objects.all()
   serializer_class = RenterSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Renter

class RenterLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email is None:
            return Response({'bool': False, 'message': 'Email is missing'} )

        password = request.data.get('password')
        if password is None:
            return Response({'bool': False, 'message': 'Password is missing'})

        renter = Renter.objects.filter(email=email, password=password).first()
        if renter:
            if renter.is_active:
                return Response({'bool': True, 'renter_id': renter.id})
            else:
                return Response({'bool': False, 'message': 'Your account is not active. Please wait for approval.'})
        else:
            return Response({'bool': False, 'message': 'Invalid email or password'})


class BlockRenterView(APIView):
    def get(self, request, pk):
        user = Renter.objects.get(id=pk)
        print(user.is_active)
        user.is_active = not user.is_active
        user.save()
        return Response({'msg': 200})
    

class UnblockRenterView(APIView):
    def put(self, request, Renter_id):
        try:
            Renter = Renter.objects.get(renter_id=Renter_id)
            Renter.is_active = True
            Renter.save()
            return Response({'message': 'Renter unblocked'})
        except Renter.DoesNotExist:
            return Response({'message': 'Renter not found'}, status=status.HTTP_404_NOT_FOUND)
