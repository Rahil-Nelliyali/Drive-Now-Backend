from django.urls import path
from . import views
from . views import  RenterLogin, RenterRegister
from .models import Renter
from .views import BlockRenterView,UnblockRenterView, RenterRegister
from .views import MyRenterTokenObtainPairView, RenterLoginView
from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', MyRenterTokenObtainPairView.as_view(), name='token_obtain_pair'),  # For sellers (renters)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Add other URL patterns for your views
    path('renterrlogin/', RenterLoginView.as_view(), name='renter_login'),
   
    path('renterlogin/', views.RenterLogin.as_view()),
    path('rentersignup/', RenterRegister.as_view()),
    path('block/<int:pk>/', BlockRenterView.as_view(), name='block_Renter'),
    path('renter/unblock/<int:renter_id>/', UnblockRenterView.as_view(), name='unblock_Renter'),
]