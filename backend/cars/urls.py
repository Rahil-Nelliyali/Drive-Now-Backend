from django.urls import path
from base.views import Singleuser
from .views import CarCategoryListCreateView, CarListCreateView, SingleCarDetailView,HomeListCar, CarDeleteView, CarUpdateView, CreateCar, CreateCarCategory, CategoryDeleteView, CategoryUpdateView, ApproveCar, RejectCar, BlockCar, MyCars
from . import views

urlpatterns = [
    path('car-category/', CarCategoryListCreateView.as_view(), name='car-category'),
    path('car/', CarListCreateView.as_view(), name='car-list-create'),
    path('home-list-car/', HomeListCar.as_view(), name='home-list-car'),
    
    path('delete-car/<int:car_id>/', CarDeleteView.as_view(), name='car-delete'),
    path('update-car/<int:car_id>/', CarUpdateView.as_view(), name='car-update'),
    path('create-car/', CreateCar.as_view(), name='car-create'),
    path('create-car-category/', CreateCarCategory.as_view(), name='car-category-create'),
    path('delete-car-category/<int:cat_id>/', CategoryDeleteView.as_view(), name='car-category-delete'),
    path('update-car-category/<int:cat_id>/', CategoryUpdateView.as_view(), name='car-category-update'),
    path('approve-car/<int:car_id>/', ApproveCar.as_view(), name='car-approve'),
    path('reject-car/<int:car_id>/', RejectCar.as_view(), name='car-reject'),
    path('block-car/<int:car_id>/', BlockCar.as_view(), name='car-block'),
    path('my-cars/<int:user_id>/', MyCars.as_view(), name='my-cars'),

    path('get-cars-by-renter/', views.get_cars_by_renter, name='get-cars-by-renter'),
    path('single-car/<int:id>/', SingleCarDetailView.as_view(), name='single_car_detail'),
    path('singleuser/<int:pk>', Singleuser.as_view(), name='singleuser'),
]