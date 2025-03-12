from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
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
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes, action
from rest_framework.renderers import JSONRenderer


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def api_home(request):
    return Response({"message": "Hello from the backend! Through Django Rest Framework!"})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])  # only for jwt authenticed users
@permission_classes([IsAuthenticated])  # checks if authenticated
def protected_view(request):
    user = request.user
    # this will return a success message, and the username of the user who send the request
    return Response({"message": f"You have access to this protected endpoint! User: {user.username}", })


# API ViewSets for CRUD Operations
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # authentication_classes = [JWTAuthentication] # could add in future to protect the view
    # permission_classes = [IsAuthenticated] # checks if anuthenticated


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
    def create(self, request):
        serializer_class = ClaimTrainingDataSerializer
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        try:
            ClaimTrainingData.objects.all().delete()
            return Response({"message": f"Claim training data has been deleted!"})
        except:
            return Response({"error": "Claim training data could not be deleted!"})


class UserClaimsViewSet(viewsets.ModelViewSet):
    queryset = UserClaims.objects.all()
    serializer_class = UserClaimsSerializer
