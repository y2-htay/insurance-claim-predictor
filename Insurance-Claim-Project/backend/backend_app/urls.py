from django.contrib import admin
from django.urls import path, include
from .views import api_home
from rest_framework.routers import DefaultRouter
from .views import (
    # api_home,  # Home API
    UserProfileViewSet, EndUserViewSet, AiEngineerViewSet,
    FinanceViewSet, AdministratorViewSet, VehicleTypeViewSet,
    WeatherConditionViewSet, ClaimTrainingDataViewSet, UserClaimsViewSet
)

router = DefaultRouter()
router.register(r'user_profiles', UserProfileViewSet)
router.register(r'end_users', EndUserViewSet)
router.register(r'ai_engineers', AiEngineerViewSet)
router.register(r'finance', FinanceViewSet)
router.register(r'administrators', AdministratorViewSet)
router.register(r'vehicle_types', VehicleTypeViewSet)
router.register(r'weather_conditions', WeatherConditionViewSet)
router.register(r'claim_training_data', ClaimTrainingDataViewSet)
router.register(r'user_claims', UserClaimsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/home/', api_home, name="api_home"),  # Home API
    path('api/', include(router.urls)),  # CRUD APIs
]