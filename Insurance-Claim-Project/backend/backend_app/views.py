from rest_framework import viewsets
from rest_framework.response import Response
from .models import (
    UserProfile, EndUser, AiEngineer, Finance, Administrator,
    VehicleType, WeatherCondition, ClaimTrainingData, UserClaims
)
from .serializers import (
    UserProfileSerializer, EndUserSerializer, AiEngineerSerializer,
    FinanceSerializer, AdministratorSerializer, VehicleTypeSerializer,
    WeatherConditionSerializer, ClaimTrainingDataSerializer, UserClaimsSerializer
)

# Home API
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def api_home(request):
    return Response({"message": "Hello from the backend! Through Django Rest Framework!"})


# API ViewSets for CRUD Operations
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class EndUserViewSet(viewsets.ModelViewSet):
    queryset = EndUser.objects.all()
    serializer_class = EndUserSerializer


class AiEngineerViewSet(viewsets.ModelViewSet):
    queryset = AiEngineer.objects.all()
    serializer_class = AiEngineerSerializer


class FinanceViewSet(viewsets.ModelViewSet):
    queryset = Finance.objects.all()
    serializer_class = FinanceSerializer


class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer


class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer


class WeatherConditionViewSet(viewsets.ModelViewSet):
    queryset = WeatherCondition.objects.all()
    serializer_class = WeatherConditionSerializer


class ClaimTrainingDataViewSet(viewsets.ModelViewSet):
    queryset = ClaimTrainingData.objects.all()
    serializer_class = ClaimTrainingDataSerializer


class UserClaimsViewSet(viewsets.ModelViewSet):
    queryset = UserClaims.objects.all()
    serializer_class = UserClaimsSerializer
