from django.contrib import admin
from django.urls import path
from .views import home, profile, login_view, logout_view, register_view, submit_claim_view, admin_dashboard, feedback_view, finance_dashboard, ai_engineer_dashboard, privacy_policy_view, terms_view, edit_or_delete_claim_view
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
    path('admin_dashboard/', admin_dashboard, name = 'admin'),
    path("feedback/", feedback_view, name="feedback"),
    path("finance_dashboard/", finance_dashboard, name="finance"),
    path('ai_engineer_dashboard/', ai_engineer_dashboard, name='ai_engineer_dashboard'),
    path('privacy_policy/', privacy_policy_view, name='privacy_policy'),
    path('terms/', terms_view, name='terms'),
    path('edit_claim/<int:claim_id>/', edit_or_delete_claim_view, name='edit_claim')


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)