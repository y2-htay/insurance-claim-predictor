from django.urls import path
from .views import api_home

urlpatterns = [
    path('api/', api_home),
]
