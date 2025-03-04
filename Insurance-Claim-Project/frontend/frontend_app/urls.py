from django.contrib import admin
from django.urls import path, include
from .views import home
from backend.backend_app import urls as backend_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]