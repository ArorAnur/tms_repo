from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('TMS_system', '0009_populate_seed_data'), # Ensure this is your correct previous file
    ]

    operations = [
        migrations.RunSQL(
            "CREATE INDEX idx_task_assignee ON tms_tasks (assignee_id);",
            "DROP INDEX idx_task_assignee ON tms_tasks;"
        ),
        migrations.RunSQL(
            "CREATE INDEX idx_userprofile_user ON TMS_system_userprofile (user_id);",
            "DROP INDEX idx_userprofile_user ON TMS_system_userprofile;"
        ),
    ]