# serializers/user_serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from ..services.user_services import register_user_pipeline

class UserRegisterSerializer(serializers.ModelSerializer):
    department = serializers.CharField(max_length=100, required=True)
    experience_years = serializers.IntegerField(required=True, min_value=0)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'department', 'experience_years']

    def create(self, validated_data):
        # Delegate all business orchestration to the service layer
        return register_user_pipeline(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            department=validated_data['department'],
            experience_years=validated_data['experience_years']
        )