from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('frontend_app/', include('frontend_app.urls')),
    path('backend_app/', include('backend_app.urls')),
]