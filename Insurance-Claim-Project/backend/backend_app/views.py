from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes, action
from rest_framework.renderers import JSONRenderer
from django.db import DatabaseError
from .models import (
    UserProfile, EndUser, AiEngineer, Finance, Administrator,
    VehicleType, WeatherCondition, ClaimTrainingData, UserClaims,
    Invoice, UsageLog, UserFeedback
)
from .serializers import (
    UserProfileSerializer, EndUserSerializer, AiEngineerSerializer,
    FinanceSerializer, AdministratorSerializer, VehicleTypeSerializer,
    WeatherConditionSerializer, ClaimTrainingDataSerializer, UserClaimsSerializer,
    InvoiceSerializer, UsageLogSerializer, UserFeedbackSerializer
)
from .utils import get_current_user, log_action
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


class ClaimTrainingDataViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAiEngineer]
    queryset = ClaimTrainingData.objects.all()
    serializer_class = ClaimTrainingDataSerializer
    parser_classes = (MultiPartParser,)  # Allow file uploads

    def create(self, request):
        """ Default create for adding a single ClaimTrainingData entry."""
        serializer_class = ClaimTrainingDataSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            user_profile = get_current_user(request)
            log_action("Added to claim training data!", user_profile)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

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
        
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsAiEngineer])
    def upload_csv(self, request):
        """ Custom action for uploading a CSV file."""
        # Check if a file is provided
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Read and process the CSV file
        try:
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            skipped_rows = [] # To track rows that are skipped
            for index, row in enumerate(reader, start=1):
                try:
                    # Handle missing or invalid vehicle_type
                    vehicle_type_id = row.get('vehicle_type')
                    if not vehicle_type_id:
                        # Skip the row or set a default value
                        skipped_rows.append({"row": index, "error": "missing vehicle_type"})
                        continue
                    vehicle_type = VehicleType.objects.get(pk=vehicle_type_id)


                    # Handle missing or invalid weather_condition
                    weather_condition_id = row.get('weather_condition')
                    if not weather_condition_id:
                        # Skip the row or set a default value
                        skipped_rows.append({"row": index, "error": "missing weather_condition"})
                        continue
                    weather_condition = WeatherCondition.objects.get(pk=weather_condition_id)
           
                    # Create ClaimTrainingData entry
                    ClaimTrainingData.objects.create(
                        settle_value=row.get('settle_value', 0),
                        accident_type=row.get('accident_type', 0),
                        injury_prognosis_months=row.get('injury_prognosis_months', 0),
                        exceptional_circumstance=row.get('exceptional_circumstance', False),
                        psychological_injury=row.get('psychological_injury', False),
                        dominant_injury=row.get('dominant_injury', 0),
                        whiplash=row.get('whiplash', False),
                        vehicle_type=vehicle_type,
                        weather_condition=weather_condition,
                        vehicle_age=row.get('vehicle_age', 0),
                        driver_age=row.get('driver_age', 0),
                        num_passengers=row.get('num_passengers', 1),
                        police_report=row.get('police_report', False),
                        witness_present=row.get('witness_present', False),
                        gender=row.get('gender', 0),
                    )
                except VehicleType.DoesNotExist:
                    skipped_rows.append({"row": index, "error": f"VehicleType with id {vehicle_type_id} does not exist"})
                except WeatherCondition.DoesNotExist:
                    skipped_rows.append({"row": index, "error": f"WeatherCondition with id {weather_condition_id} does not exist"})

                
            return Response({
                "message": "CSV file processed successfully",
                "skipped_rows": skipped_rows,
            }, status=status.HTTP_200_OK)
        
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
