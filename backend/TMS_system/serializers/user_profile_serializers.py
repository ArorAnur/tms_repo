from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['department', 'experience_years', 'active_tasks_count']

class UserSerializer(serializers.ModelSerializer):
    # Nest the profile serializer inside the main user serializer
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

