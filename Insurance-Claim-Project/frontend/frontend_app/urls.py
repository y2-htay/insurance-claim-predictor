from django.contrib import admin
from django.urls import path
from .views import home, profile, login_view, logout_view, register_view, submit_claim_view, feedback_view
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path('profile/', profile, name = 'profile'),
    path('submit_claim/', submit_claim_view, name = 'submit_claim'),
    path("feedback/", feedback_view, name="feedback"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)