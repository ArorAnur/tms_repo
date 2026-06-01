from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Links directly to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Static attributes for the assignment engine
    department = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    
    # Dynamic metric tracked by your worker system
    active_tasks_count = models.IntegerField(default=0)

    class Meta:
        app_label = 'TMS_system'
        db_table = 'TMS_system_userprofile'
        indexes = [
            models.Index(
                fields=['department', 'active_tasks_count', 'experience_years'],
                name='idx_dept_tasks_exp'
            ),
        ]

    def __str__(self):
        return f"{self.user.username}'s Profile"