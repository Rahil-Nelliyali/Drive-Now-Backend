from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("base.urls")),
    path("api-renter/", include("renter.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("cars/", include("cars.urls")),
    path("payment/", include("payment.urls")),
    path("", include("chat.urls")),
]
