from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes, action
from rest_framework.renderers import JSONRenderer
from django.db import DatabaseError
from .models import (
    UserProfile, EndUser, AiEngineer, Finance, Administrator,
    VehicleType, WeatherCondition, ClaimTrainingData, UserClaims,
    Invoice
)
from .serializers import (
    UserProfileSerializer, EndUserSerializer, AiEngineerSerializer,
    FinanceSerializer, AdministratorSerializer, VehicleTypeSerializer,
    WeatherConditionSerializer, ClaimTrainingDataSerializer, UserClaimsSerializer,
    InvoiceSerializer
)
from .logging import log_action
from .utils import get_current_user
from .ai_model import train_new_model


# Home API
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

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = UserProfileSerializer
        serializer_class.save()
        log_action("Created a new user profile!", user_profile)
    # authentication_classes = [JWTAuthentication] # could add in future to protect the view
    # permission_classes = [IsAuthenticated] # checks if anuthenticated


class EndUserViewSet(viewsets.ModelViewSet):
    queryset = EndUser.objects.all()

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = EndUserSerializer
        serializer_class.save()
        log_action("Created a new end-user account!", user_profile)


class AiEngineerViewSet(viewsets.ModelViewSet):
    queryset = AiEngineer.objects.all()

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = AiEngineerSerializer
        serializer_class.save()
        log_action("Created a new ai-engineer account!", user_profile)


class FinanceViewSet(viewsets.ModelViewSet):
    queryset = Finance.objects.all()

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = FinanceSerializer
        serializer_class.save()
        log_action("Created a new finance account!", user_profile)


class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = AdministratorSerializer
        serializer_class.save()
        log_action("Created a new admin account!", user_profile)


class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer

    def create(self, request):
        serializer_class = VehicleTypeSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            user_profile = get_current_user(request)
            log_action("Created a new vehicle type!", user_profile)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class WeatherConditionViewSet(viewsets.ModelViewSet):
    queryset = WeatherCondition.objects.all()
    serializer_class = WeatherConditionSerializer

    def create(self, request):
        serializer_class = WeatherConditionSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            user_profile = get_current_user(request)
            log_action("Created a new weather condition!", user_profile)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class ClaimTrainingDataViewSet(viewsets.ModelViewSet):
    def create(self, request):
        serializer_class = ClaimTrainingDataSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            user_profile = get_current_user(request)
            log_action("Added to claim training data!", user_profile)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        user_profile = get_current_user(request)
        try:
            ClaimTrainingData.objects.all().delete()
            log_action("Deleted all claim training data!", user_profile)
            return Response({"message": f"Claim training data has been deleted!"})
        except DatabaseError:
            return Response({"error": "Claim training data could not be deleted!"})


class UserClaimsViewSet(viewsets.ModelViewSet):
    queryset = UserClaims.objects.all()

    def create(self, request):
        serializer_class = UserClaimsSerializer
        user_profile = get_current_user(request)
        serializer_class.save()
        log_action("User claim created", user_profile)

    def create(self, request, *args, **kwargs):
        # on creatine of user claim, serialize with request
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # save the user claim request with the associated user !
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# invoice view
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def create(self, request):
        user_id = request.data.get("user_id")
        try:
            user = UserProfile.objects.get(id=user_id)  # check user exists
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # get claims for the user
        claims = UserClaims.objects.filter(user=user)
        if not claims.exists():
            return Response({"error": "No claims found for this user"}, status=status.HTTP_400_BAD_REQUEST)

        # create invoice and calculate total
        invoice = Invoice.objects.create(user=user)
        log_action("Invoice created!", user)
        invoice.calculate_total()

        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)


class TrainModelViewSet(viewsets.ModelViewSet):
    queryset = ClaimTrainingData.objects.all()

    @action(detail=False, methods=['post'])
    def train_model(self, request):
        training_data = ClaimTrainingData.objects.all().values()
        train_new_model(training_data)
        # url stuff
        return Response({"status": "Model training initiated"})
