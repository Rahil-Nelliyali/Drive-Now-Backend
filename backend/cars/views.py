from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from cars.models import Car, CarCategory
from base.models import User
from renter.models import Renter
from .serializers import CarSerializer, CarCategorySerializer, PostCarSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics

class CarCategoryListCreateView(generics.ListCreateAPIView):
    
    serializer_class = CarCategorySerializer
    def get_queryset(self):
        # Get the logged-in seller's ID (renter ID) from the request's user
        renter_id = self.request.user.id
        print("Logged-in Renter ID:", renter_id)   # Filter the queryset to show only categories created by the logged-in seller
        queryset = CarCategory.objects.filter(renter_id=renter_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(renter=self.request.user)

class CarListCreateView(generics.ListCreateAPIView):
    
    serializer_class = CarSerializer
    def get_queryset(self):
        # Get the logged-in seller's ID (renter ID) from the request's user
        renter_id = self.request.user.id
        print("Logged-in Renter ID:", renter_id)   # Filter the queryset to show only categories created by the logged-in seller
        queryset = Car.objects.filter(renter_id=renter_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(renter=self.request.user)

class HomeListCar(APIView):
    def get(self, request):
        queryset = Car.objects.filter(is_active=True)
        serializer = CarSerializer(queryset, many=True)
        return Response(serializer.data)


class CarDeleteView(APIView):
    def delete(self, request, car_id):
        queryset = Car.objects.filter(id=car_id)
        queryset.delete()
        return Response({'msg': 'Car deleted successfully'})




class CarUpdateView(APIView):
    def patch(self, request, car_id):
        try:
            Car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"msg": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostCarSerializer(Car, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Car updated successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateCar(APIView):
    def post(self, request, format=None):
        serializer = PostCarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Car created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, car_id=None):
        if car_id is not None:
            queryset = Car.objects.get(id=car_id)
            serializer = CarSerializer(queryset)
            return Response(serializer.data)
        return Response({'msg': 'Car not found'}, status=404)

class CreateCarCategory(APIView):
    def post(self, request, format=None):
        serializer = CarCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Car category created'}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Add this line to print the serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    def delete(self, request, cat_id):
        queryset = CarCategory.objects.get(id=cat_id)
        queryset.delete()
        return Response({'msg': 'Category deleted successfully'})


class CategoryUpdateView(APIView):
    def get(self, request, cat_id):
        category = CarCategory.objects.get(id=cat_id)
        serializer = CarCategorySerializer(category, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Category updated successfully"})
        else:
            return Response(serializer.errors)


    

class ApproveCar(APIView):
    def get(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"msg": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        car.is_approved = True
        car.save()
        return Response({"msg": "Car approved"})

class RejectCar(APIView):
    def get(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"msg": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        car.is_approved = False
        car.save()
        return Response({"msg": "Car rejected"})

class BlockCar(APIView):
    def get(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"msg": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        car.is_approved = not car.is_approved
        car.save()
        return Response({"msg": "Car block status updated"})


class MyCars(APIView):
    def get(self, request, user_id):
        try:
            user = Renter.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        cars = Car.objects.filter(user=user)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)
    


@api_view(['GET'])
def get_cars_by_renter(request):
    renter_id = request.user.id  # Assuming you are using TokenAuthentication or SessionAuthentication
    cars = Car.objects.filter(renter_id=renter_id)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class SingleCarDetailView(RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'id'