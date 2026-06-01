# tasks.py
from celery import shared_task
from django.db import transaction
from django.contrib.auth.models import User
from ..models import Task
from ..models import UserProfile
from django.db.models import F


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def process_task_assignment_async(self, task_id):
    try:
        task = Task.objects.get(task_id=task_id)
        
        if task.status == 'assigned':
            return f"Task {task_id} is already assigned."
            
        rules = task.assignment_rules
        if not rules:
            task.status = 'unassigned_no_match'
            task.save()
            return f"Task {task_id} has no rules."

        # Define allowed fields to prevent arbitrary query injection
        ALLOWED_FIELDS = {'department', 'experience_years', 'active_tasks_count'} 

        # 1. Dynamically build the SQL filter query
        query_filters = {}
        lookup_map = {
            'EQUALS': '',
            'GREATER_THAN_OR_EQUAL': '__gte',
            'LESS_THAN': '__lt'
        }

        for rule in rules:
            field = rule.get('field')
            if field in ALLOWED_FIELDS:
                suffix = lookup_map.get(rule.get('operator'), '')
                query_filters[f"{field}{suffix}"] = rule.get('value')

        # 2. Execute a SINGLE database query
        # Build and execute the candidate query inside the transaction to safely lock rows.

        # 3. Atomic transaction block with row-level locking
        with transaction.atomic():
            # Find the best candidate and lock their row to prevent concurrent assignment.
            best_candidate = (
                UserProfile.objects.select_for_update(skip_locked=True)
                .filter(**query_filters)
                .order_by('active_tasks_count')
                .first()
            )

            if not best_candidate:
                task.status = 'unassigned_no_match'
                task.save()
                return f"No matching candidates found for Task {task_id}."

            # Re-fetch and lock the task to ensure it hasn't been assigned by another worker.
            task = Task.objects.select_for_update().get(task_id=task_id)

            if task.status == 'assigned':
                return f"Task {task_id} already handled by another worker."

            # Assign the task and update the candidate's active task count.
            task.assignee_id = best_candidate.user_id
            task.status = 'assigned'
            task.save()

            best_candidate.active_tasks_count = F('active_tasks_count') + 1
            best_candidate.save()

        return f"Successfully assigned Task {task_id} to User {best_candidate.user_id}"

    except Task.DoesNotExist:
        return f"Task {task_id} missing."
    except Exception as exc:
        raise self.retry(exc=exc)