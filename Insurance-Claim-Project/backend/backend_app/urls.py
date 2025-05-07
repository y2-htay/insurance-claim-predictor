from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView  # jwt djoser
from .views import *

router = DefaultRouter()
router.register(r'user_profiles', UserProfileViewSet)
router.register(r'end_users', EndUserViewSet)
router.register(r'ai_engineers', AiEngineerViewSet)
router.register(r'finance', FinanceViewSet)
router.register(r'administrators', AdministratorViewSet)
router.register(r'vehicle_types', VehicleTypeViewSet)
router.register(r'weather_conditions', WeatherConditionViewSet)
router.register(r'claim_training_data', ClaimTrainingDataViewSet, basename='claimtrainingdata')
router.register(r'user_claims', UserClaimsViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'train_model', TrainModelViewSet, basename='trainmodel')
router.register(r'usage_logs', UsageLogViewSet, basename='usage_logs')
router.register(r'user_feedback', UserFeedbackViewSet)
router.register(r'gender', GenderViewSet, basename='gender')
router.register(r'injury_description', InjuryDescriptionViewSet, basename='injury_description')
router.register(r'insurance_models', InsuranceModelViewSet, basename='insurance_models')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/home/', api_home, name="api_home"),  # Home API
    path('api/protected/', protected_view, name='protected_view'),  # jwt protected view
    path('api/', include(router.urls)),  # CRUD APIs
    path('api/auth/', include('djoser.urls')),
    # this include /api/auth/users/, /api/auth/jwt/create/ etc. see documentation
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/upload-training-data', include('djoser.urls.jwt'), name="ai_data"),
    path('api/train_model', include('djoser.urls.jwt'), name="ai_train"),
    path('api/realtime-graph/', serve_realtime_graph, name='serve_realtime_graph'),

]
