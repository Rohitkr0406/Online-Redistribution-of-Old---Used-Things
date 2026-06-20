from django.db import connection
from django.utils import timezone

def log_admin_action(admin_id, action, details=""):
    """
    Helper function to record admin actions into the admin_audit_logs table.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO admin_audit_logs (AdminID, Action, Details, Timestamp) VALUES (%s, %s, %s, %s)",
                [admin_id, action, details, timezone.now()]
            )
    except Exception as e:
        print(f"Error logging admin action ({admin_id}, {action}): {str(e)}")
