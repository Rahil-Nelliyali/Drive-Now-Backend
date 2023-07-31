from django.urls import path
from . import views
from . views import RenterList, RenterLogin, RenterRegister
from .models import Renter
from .views import BlockRenterView,UnblockRenterView, RenterRegister


urlpatterns = [
    path('renter/', views.RenterList.as_view()),
    path('renter/<int:pk>/', views.RenterDetail.as_view()),
    path('renterlogin/', views.RenterLogin.as_view()),
    path('rentersignup/', RenterRegister.as_view()),
    path('block/<int:pk>/', BlockRenterView.as_view(), name='block_Renter'),
    path('renter/unblock/<int:renter_id>/', UnblockRenterView.as_view(), name='unblock_Renter'),
]