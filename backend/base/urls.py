from django.urls import path
from . import views
from .views import (
    AuthView,
    UserRegistration,
    Listuser,
    GetProfile,
    UpdateProfile,
    ChangePass,
    ChangeImage,
    BlockUserView,
    RenterRegistration,
    Listrenter,
    BlockRenterView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)


urlpatterns = [
    path("", views.getRoutes),
    path("auth/", AuthView.as_view(), name="auth"),
    path("token/", AuthView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegistration.as_view()),
    path("renterregister/", RenterRegistration.as_view()),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path(
        "activaterenter/<uidb64>/<token>", views.activaterenter, name="activaterenter"
    ),
    path("users/", Listuser.as_view(), name="users"),
    path("blockuser/<int:pk>/", BlockUserView.as_view(), name="block-user"),
    path("renters/", Listrenter.as_view(), name="renters"),
    path("blockrenter/<int:pk>/", BlockRenterView.as_view(), name="block-user"),
    path("profile/<int:pk>", GetProfile.as_view(), name="profile"),
    path("updateprofile/", UpdateProfile.as_view(), name="updateprofile"),
    path("changepass/", ChangePass.as_view(), name="changepass"),
    path("updateimage/", ChangeImage.as_view(), name="updateimage"),
    path(
        "getSingleUser/<int:id>/", views.GetSingleUser.as_view(), name="getDoctorInHome"
    ),
]
