# services/task_services.py
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
from ..models import (
    Task,
    TaskStatus,
    UserProfile,
)  # Go up one level to find the models package
from ..tasks import process_task_assignment_async
from django.db.models import F
import logging

logger = logging.getLogger(__name__)


def create_new_task(
    title,
    description=None,
    assignee_id=None,
    completion_date=None,
    assignment_rules=None,
):
    # 1. Domain Validation Rules
    if completion_date and completion_date < timezone.now():
        raise ValueError("The completion target date cannot be set in the past.")

    if assignee_id is not None:
        if not completion_date:
            raise ValueError(
                "An explicit completion date is mandatory when assigning a task."
            )
        target_status = TaskStatus.ASSIGNED
        assignee_user = User.objects.get(id=assignee_id)
    else:
        # If no explicit assignee is forced, it defaults to UNASSIGNED and looks for rules
        target_status = TaskStatus.UNASSIGNED
        assignee_user = None

    # 2. Atomic Database Insertion Block
    with transaction.atomic():
        task = Task.objects.create(
            title=title,
            description=description,
            assignee=assignee_user,
            assignment_rules=assignment_rules or [],
            completion_date=completion_date,
            status=target_status,
        )

    # 3. Asynchronous Workflow Hand-off
    # If the task has rules and is waiting for dynamic system routing (UNASSIGNED)
    if task.status == TaskStatus.UNASSIGNED and task.assignment_rules:
        # transaction.on_commit forces Django to wait until MySQL completely finishes
        # committing the row write before firing the task message over to the Redis broker.
        transaction.on_commit(lambda: process_task_assignment_async.delay(task.task_id))

    return task


def recompute_task_eligibility(task_id, new_rules):
    """
    Business logic to unassign a task safely, update its rules, decrement
    the previous owner's workload counter, and trigger async re-assignment.
    """
    with transaction.atomic():
        # Lock the task row immediately to prevent race conditions from concurrent workers
        task = Task.objects.select_for_update().get(pk=task_id)

        logger.info(
            f"task referred is: {task.task_id}   for user {task.assignee.username}"
        )

        # Domain Guard Rail: Cannot recompute a completed task
        if getattr(task, "status", None) == "completed":
            raise ValueError(
                "Cannot recompute a task that has already been marked completed."
            )

        # If currently assigned, safely decrement the previous owner's workload metrics
        if task.assignee:
            UserProfile.objects.select_for_update().filter(
                user=task.assignee, active_tasks_count__gt=0
            ).update(active_tasks_count=F("active_tasks_count") - 1)

        # Apply the new rules configuration and reset structural state pointers
        task.assignee = None
        task.status = TaskStatus.UNASSIGNED
        task.assignment_rules = new_rules
        task.save()

    # Offload heavy calculations to Celery after the database transaction block fully commits
    transaction.on_commit(lambda: process_task_assignment_async.delay(task.task_id))

    return task


def mark_task_completed(task_id, user):
    """
    Business logic to mark a task as completed, ensuring only the assigned user can perform this action.
    Also decrements the user's active workload counter if applicable.
    """
    with transaction.atomic():
        task = Task.objects.select_for_update().get(pk=task_id)

        # Domain Guard Rail: Only the assigned user can mark the task as completed
        if task.assignee != user:
            raise ValueError("You are not authorized to complete this task.")

        if task.status == "completed":
            return

        task.status = "completed"
        task.save()

        # If the task was previously assigned, decrement the user's active workload counter
        if task.assignee:
            profile = UserProfile.objects.select_for_update().get(user=task.assignee)
            if profile.active_tasks_count > 0:
                profile.active_tasks_count -= 1
                profile.save()

        return task
