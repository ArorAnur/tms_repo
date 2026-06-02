from django.db import models
from django.contrib.auth.models import User

class TaskStatus(models.TextChoices):
    UNASSIGNED = 'UNASSIGNED', 'Unassigned'
    ASSIGNED = 'ASSIGNED', 'Assigned'
    DONE = 'COMPLETED', 'Completed'

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assignment_rules = models.JSONField(default=list, blank=True, null=True)
    
    assignee = models.ForeignKey(
    User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='tasks',
        db_index=True
    )
    
    completion_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.UNASSIGNED
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      
        app_label = 'TMS_system'
        db_table = 'tms_tasks'

    def __str__(self):
        return f"Task #{self.task_id}: {self.title} ({self.status})"    