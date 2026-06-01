from django.db import transaction
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Task, TaskStatus
from ..permissions import HasRequiredScope
from ..serializers import (
    RecomputeEligibilitySerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
)
from ..services import create_new_task, recompute_task_eligibility, mark_task_completed
from ..tasks import process_task_assignment_async


class CreateTaskView(APIView):
    """
    API view for creating new tasks with optional assignment rules.
    
    Requires JWT authentication. Accepts task details and optional
    assignment rules for automated task assignment workflows.
    """
    permission_classes = [IsAuthenticated, HasRequiredScope]
    required_scope = 'write'

    def post(self, request):
        """
        Create a new task with the provided details.
        
        Args:
            request: HTTP request containing task data
            
        Returns:
            Response: Created task details or validation errors
        """
        serializer = TaskCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                task = create_new_task(
                    title=serializer.validated_data['title'],
                    description=serializer.validated_data.get('description', ''),
                    assignee_id=serializer.validated_data.get('assignee_id'),
                    completion_date=serializer.validated_data.get('completion_date'),
                    assignment_rules=serializer.validated_data.get('assignment_rules'),
                )
                return Response(
                    {'message': 'Task created successfully', 'task_id': task.task_id},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# views.py


class MarkTaskCompletedView(APIView):
    """
    API view to mark a task as completed by the assigned user.
    Enforces that only the assignee can perform this action.
    """
    permission_classes = [IsAuthenticated, HasRequiredScope]
    required_scope = 'read'

    def put(self, request, task_id):
        try:
            updated_task = mark_task_completed(task_id, request.user)
            return Response(
                {
                    "message": "Task marked as completed successfully.",
                    "task_id": updated_task.task_id,
                    "status": updated_task.status
                },
                status=status.HTTP_200_OK
            )
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





class MyEligibleTasksView(APIView):
    """
    API View to retrieve all tasks assigned to the authenticated user.
    Supports high-scale volume via standard Limit-Offset Pagination.
    """
    permission_classes = [IsAuthenticated, HasRequiredScope]
    required_scope = 'read'  # Enforces that the JWT contains the 'read' scope claim

    def get(self, request):
        # 1. Fetch tasks assigned directly to the calling user
        # This performs an indexed lookup on the foreign key column in MySQL
        queryset = Task.objects.filter(assignee=request.user).order_by('-created_at')

        # 2. Apply standard DRF Pagination to preserve server memory bounds
        paginator = LimitOffsetPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)
        
        # 3. Serialize and return the formatted page split frame
        serializer = TaskDetailSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    






class RecomputeEligibilityView(APIView):
    """
    Administrative gateway to reset and evaluate task matching rules.
    Business domain execution is completely delegated to the service layer.
    """
    permission_classes = [IsAuthenticated, HasRequiredScope]
    required_scope = 'admin'  # Strictly requires admin-level scope authorization

    def post(self, request, task_id):
        # 1. Ingest and validate incoming rules format
        serializer = RecomputeEligibilitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_rules = serializer.validated_data['assignment_rules']

        # 2. Delegate to the service layer domain execution
        try:
            updated_task = recompute_task_eligibility(task_id, new_rules)
            
            return Response(
                {
                    "message": "Task successfully unassigned and queued for eligibility re-computation.",
                    "task_id": updated_task.task_id,
                    "status": updated_task.status
                },
                status=status.HTTP_200_OK
            )

        except Task.DoesNotExist:
            return Response({"error": "Target task record not found."}, status=status.HTTP_404_NOT_FOUND)
            
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)