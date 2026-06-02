from django.db import migrations
from django.contrib.auth.hashers import make_password
from itertools import cycle

def create_initial_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('TMS_system', 'UserProfile')

    # 1. Create the Admin Superuser
    User.objects.create(
        username='admin',
        email='admin@tms.com',
        is_staff=True,
        is_superuser=True,
        password=make_password('admin123')
    )

    # 2. Setup Data for standard users
    names = ['alice', 'bob', 'charlie', 'diana', 'eve', 'frank', 'grace', 'heidi', 'ivan', 'judy']
    departments = cycle(['Engineering', 'HR', 'Operations', 'Design'])
    
    # 3. Create 10 Standard Users
    for i, name in enumerate(names):
        user = User.objects.create(
            username=name,
            email=f'{name}@tms.com',
            is_staff=False,
            is_superuser=False,
            password=make_password('password123')
        )
        UserProfile.objects.create(
            user=user,
            department=next(departments),
            experience_years=i + 1,  # 1 to 10 years experience
            active_tasks_count=0
        )

class Migration(migrations.Migration):
    dependencies = [
        ('TMS_system', '0008_alter_userprofile_table'), # Ensure this is your correct previous file
    ]
    operations = [
        migrations.RunPython(create_initial_data),
    ]