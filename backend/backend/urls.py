from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/', include('base.urls')),
    path('api-renter/',include('renter.urls')),
    path('api-auth/',include('rest_framework.urls')),
    path('cars/',include('cars.urls')),
    path('payment/',include('payment.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
