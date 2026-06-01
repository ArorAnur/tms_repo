# services/user_services.py
from django.db import transaction
from django.contrib.auth.models import User
from ..models import UserProfile

def register_user_pipeline(username: str, email: str, password: str, department: str, experience_years: int) -> User:
    """
    Orchestrates the entire business transaction for registering a user
    across multiple separate tables.
    """
    with transaction.atomic():
        # 1. Create the Auth User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 2. Create the User Profile
        UserProfile.objects.create(
            user=user,
            department=department,
            experience_years=experience_years,
            active_tasks_count=0
        )
        
        # 3. Future Expansion: Trigger email verification, 
        # notify downstream analytics systems, or trigger worker syncs here.
        
    return user