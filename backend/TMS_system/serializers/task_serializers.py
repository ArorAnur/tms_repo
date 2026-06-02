# serializers/task_serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Task # Note the double dot (..) to go up out of serializers/
from .user_profile_serializers import UserSerializer
class TaskCreateSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    assignee_id = serializers.IntegerField(required=False, allow_null=True)
    completion_date = serializers.DateTimeField(required=False, allow_null=True)
    assignment_rules = serializers.ListField(
        child=serializers.JSONField(), required=False, allow_null=True
    )

    def validate_assignee_id(self, value):
        if value and not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("The targeted assignee user does not exist.")
        return value
    



class TaskDetailSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    class Meta:
        model = Task
        fields = [
            'task_id', 
            'title', 
            'description', 
            'status', 
            'completion_date', 
            'assignment_rules', 
            'created_at',
            'assignee',
        ]
        read_only_fields = fields

class MarkTaskCompletedSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=True)   

     


class RecomputeEligibilitySerializer(serializers.Serializer):
    assignment_rules = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False,
        help_text="The updated rule array payload to evaluate against candidate user profiles."
    )