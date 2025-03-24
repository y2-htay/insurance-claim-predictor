from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import (
    UserProfile, EndUser, AiEngineer, Finance, Administrator,
    VehicleType, WeatherCondition, ClaimTrainingData, UserClaims, Invoice,
    UsageLog, Actions
)


# serializer for user REGISTRATION
class UserProfileCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserProfile
        fields = ('id', 'username', 'password', 'permission_level')


# serializer for user retrieval using djoser
class UserProfileAuthSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserProfile
        fields = ('id', 'username', 'password', 'permission_level')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class EndUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUser
        fields = '__all__'


class AiEngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiEngineer
        fields = '__all__'


class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = '__all__'


class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'


class WeatherConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCondition
        fields = '__all__'


class ClaimTrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimTrainingData
        fields = '__all__'


class UserClaimsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClaims
        fields = '__all__'


# invoice
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


# usage log serializer 
class UsageLogSerializer(serializers.ModelSerializer):
    action_text = serializers.CharField(source='action.action', read_only=True)  # get associated action text to given log
    username = serializers.CharField(source='user.username', read_only=True) # get associated username to given log
    
    class Meta:
        model = UsageLog
        fields = ['id', 'user', 'username', 'action_text', 'time'] # return necessary display detaiils