from django.contrib import admin
from django.urls import path
from .views import home, profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('profile/', profile, name = 'profile'),
]