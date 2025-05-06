import pandas as pd
from django.db import DatabaseError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .ai_model import train_new_model
from .permissions import *
from .serializers import *
from .utils import get_current_user, log_action, preprocess_data_and_upload
from rest_framework.permissions import SAFE_METHODS, BasePermission
from backend_app.ML_model.model_utils import predict_settlement, preprocess_input
import os
import csv
import subprocess


NEW_CLAIM_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ML_model", "new_claim.csv")


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

class ReadOnlyUnlessAiEngineer(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and IsAiEngineer().has_permission(request, view)
    
class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [ReadOnlyUnlessAiEngineer]

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
    permission_classes = [ReadOnlyUnlessAiEngineer]

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
    permission_classes = [ReadOnlyUnlessAiEngineer]

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

    def create(self, request):
        user_profile = get_current_user(request)
        file = request.FILES.get('file')
        try:
            data = pd.read_csv(file)
            preprocess_data_and_upload(data)
            log_action("New training data uploaded!", user_profile)
            train_new_model()
            return Response({"message": "CSV file uploaded successfully!"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

class UserClaimsViewSet(viewsets.ModelViewSet):
    queryset = UserClaims.objects.all()
    serializer_class = UserClaimsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = get_current_user(self.request)
        return UserClaims.objects.filter(user=user_profile)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user_profile = get_current_user(request)

        if serializer.is_valid():
            instance = serializer.save(user=user_profile)

            data_for_model = {
                "Driver Age": float(instance.driver_age),
                "Vehicle Age": float(instance.vehicle_age),
                "Injury_Prognosis": float(instance.injury_prognosis),
                "Vehicle Type": instance.vehicle_type.vehicle_name if instance.vehicle_type else "",
                "Weather Conditions": instance.weather_condition.condition if instance.weather_condition else "",
                "Gender": instance.gender.gender if instance.gender else "",
                "Accident Date": str(instance.accident_date),
                "Claim Date": str(instance.claim_date),
                "TotalSpecialCosts": float(instance.total_special_costs),
                "GeneralRest": float(instance.general_rest),
                "GeneralFixed": float(instance.general_fixed),
                "Number of Passengers": float(instance.passengers_involved),
                "GeneralUplift": 0.0,
                "Whiplash": int(instance.whiplash),
                "Exceptional_Circumstances": int(instance.exceptional_circumstance),
                "Witness Present": int(instance.witness_present),
                "Minor_Psychological_Injury": int(instance.psychological_injury),
            }

            try:
                prediction = predict_settlement(data_for_model)
                instance.predicted_settlement_value = prediction
                instance.save(update_fields=["predicted_settlement_value"])

                try:
                    preprocessed_df = preprocess_input(data_for_model)
                    os.makedirs(os.path.dirname(NEW_CLAIM_PATH), exist_ok=True)

        
                    

                    with open(NEW_CLAIM_PATH, "a", newline="") as csvfile:
                        row_data = preprocessed_df.iloc[0].to_dict()
                        row_data["PredictedSettlementValue"] = prediction
                        writer = csv.DictWriter(csvfile, fieldnames=row_data.keys())

                        if csvfile.tell() == 0:
                            writer.writeheader()
                        writer.writerow(row_data)

                    print("[DEBUG] Claim written to CSV")

                except Exception as write_err:
                    print("[ERROR]  Failed to write claim to CSV:", write_err)

                try:
                    subprocess.run(
                        ["python", "backend_app/ML_model/evaluate_model.py"],
                        check=True
                    )
                    print("[DEBUG]  Evaluation script ran successfully")
                except subprocess.CalledProcessError as eval_err:
                    print("[ERROR]  Evaluation script failed ", eval_err)

            except Exception as e:
                print("Prediction error:", e)

            log_action("User Claim Uploaded!", user_profile)
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class UserClaimsViewSet(viewsets.ModelViewSet):
#     queryset = UserClaims.objects.all()
#     serializer_class = UserClaimsSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user_profile = get_current_user(self.request)
#         return UserClaims.objects.filter(user=user_profile)

#     def create(self, request, *args, **kwargs):
#         # on creatine of user claim, serialize with request
#         serializer = self.get_serializer(data=request.data)
#         user_profile = get_current_user(request)
#         if serializer.is_valid():
#             # save the user claim request with the associated user !
#             serializer.save(user=request.user)
#             log_action("User Claim Uploaded!", user_profile)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        train_new_model()
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
    

