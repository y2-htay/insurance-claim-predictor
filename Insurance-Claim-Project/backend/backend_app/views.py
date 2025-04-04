import pandas as pd
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes, action
from rest_framework.renderers import JSONRenderer
from django.db import DatabaseError
from .models import *
from .serializers import *
from .utils import get_current_user, log_action, preprocess_data_and_upload
from .permissions import *
from .ai_model import train_new_model
import csv
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status


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
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = UserProfileSerializer
        serializer_class.save()
        log_action("Created a new user profile!", user_profile)

    def destroy(self, request, pk=None):
        try:
            user = UserProfile.objects.get(pk=pk)
            user.delete()
            log_action("User profile deleted successfully.", None)
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EndUserViewSet(viewsets.ModelViewSet):
    queryset = EndUser.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = EndUserSerializer
        serializer_class.save()
        log_action("Created a new end-user account!", user_profile)


class AiEngineerViewSet(viewsets.ModelViewSet):
    queryset = AiEngineer.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = AiEngineerSerializer
        serializer_class.save()
        log_action("Created a new ai-engineer account!", user_profile)


class FinanceViewSet(viewsets.ModelViewSet):
    queryset = Finance.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = FinanceSerializer
        serializer_class.save()
        log_action("Created a new finance account!", user_profile)


class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user_profile = get_current_user(request)
        serializer_class = AdministratorSerializer
        serializer_class.save()
        log_action("Created a new admin account!", user_profile)


class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAiEngineer]

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAiEngineer]

    def create(self, request):
        serializer_class = WeatherConditionSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            user_profile = get_current_user(request)
            log_action("Created a new weather condition!", user_profile)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAiEngineer]

    def create(self, request):
        serializer_class = GenderSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            user_profile = get_current_user(request)
            log_action("Created a new gender!", user_profile)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class InjuryDescriptionViewSet(viewsets.ModelViewSet):
    queryset = InjuryDescription.objects.all()
    serializer_class = InjuryDescriptionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAiEngineer]

    def create(self, request):
        serializer_class = InjuryDescriptionSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            user_profile = get_current_user(request)
            log_action("Created a new injury description!", user_profile)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class ClaimTrainingDataViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAiEngineer]
    queryset = ClaimTrainingData.objects.all()
    serializer_class = ClaimTrainingDataSerializer
    parser_classes = (MultiPartParser,)  # Allow file uploads

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        """ Default delete for removing all ClaimTrainingData entries."""
        user_profile = get_current_user(request)
        try:
            ClaimTrainingData.objects.all().delete()
            log_action("Deleted all claim training data!", user_profile)
            return Response({"message": "Claim training data has been deleted!"})
        except DatabaseError:
            return Response({"error": "Claim training data could not be deleted!"})

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def upload_csv(self, request):
        user_profile = get_current_user(request)
        file = request.FILES.get('file')
        try:
            data = pd.read_csv(file)
            preprocess_data_and_upload(data)
            log_action("New training data uploaded!", user_profile)
            return Response({"message": "CSV file uploaded successfully!"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserClaimsViewSet(viewsets.ModelViewSet):
    queryset = UserClaims.objects.all()
    serializer_class = UserClaimsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = get_current_user(self.request)
        return UserClaims.objects.filter(user=user_profile)

    def create(self, request, *args, **kwargs):
        # on creatine of user claim, serialize with request
        serializer = self.get_serializer(data=request.data)
        user_profile = get_current_user(request)
        if serializer.is_valid():
            # save the user claim request with the associated user !
            serializer.save(user=request.user)
            log_action("User Claim Uploaded!", user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# invoice view
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAiEngineer]

    @action(detail=False, methods=['post'])
    def train_model(self, request):
        training_data = ClaimTrainingData.objects.all().values()
        train_new_model(training_data)
        # url stuff
        return Response({"status": "Model training initiated"})


# usage logs viewset - to display on the admin dashboard

class UsageLogViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdministrator]

    def list(self, request):
        user_id = request.query_params.get('user_id', None)  # get user id

        if user_id:
            logs = UsageLog.objects.filter(user__id=user_id)  # filter logs by user if user_id is provided
        else:
            logs = UsageLog.objects.all()  # otherwise fetch all logs

        serializer = UsageLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# feedback view
class UserFeedbackViewSet(viewsets.ModelViewSet):
    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            try:
                user_profile = get_current_user(request)
                log_action("User submitted feedback", user_profile)
            except Exception as e:
                print(f"Logging failed: {e}")  # optional logging fallback

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
