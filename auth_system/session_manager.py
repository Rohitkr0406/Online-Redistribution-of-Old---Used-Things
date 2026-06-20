from django.db import connection
from django.utils import timezone
import datetime

def start_admin_session(request, admin_id, admin_name):
    """
    Starts a secure admin session, saving credentials in Django session
    and inserting/updating the session tracking table in the database.
    """
    if not request.session.session_key:
        request.session.create()
    
    session_key = request.session.session_key
    
    # Store in Django session
    request.session['admin_id'] = admin_id
    request.session['admin_name'] = admin_name
    request.session['user_role'] = 'admin'
    request.session['admin_last_activity'] = timezone.now().timestamp()
    
    # Track session in database
    now = timezone.now()
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM admin_sessions WHERE SessionID = %s", [session_key])
        exists = cursor.fetchone()[0] > 0
        if exists:
            cursor.execute(
                "UPDATE admin_sessions SET AdminID = %s, LoginTime = %s, LastActivity = %s, LogoutTime = NULL WHERE SessionID = %s",
                [admin_id, now, now, session_key]
            )
        else:
            cursor.execute(
                "INSERT INTO admin_sessions (SessionID, AdminID, LoginTime, LastActivity) VALUES (%s, %s, %s, %s)",
                [session_key, admin_id, now, now]
            )

def update_admin_activity(request):
    """
    Updates the admin's last activity timestamp in the session and database.
    """
    if 'admin_id' in request.session:
        now = timezone.now()
        request.session['admin_last_activity'] = now.timestamp()
        
        session_key = request.session.session_key
        if session_key:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE admin_sessions SET LastActivity = %s WHERE SessionID = %s",
                    [now, session_key]
                )

def logout_admin(request):
    """
    Logs out the admin, recording the logout timestamp in the database and clearing session keys.
    """
    session_key = request.session.session_key
    admin_id = request.session.get('admin_id')
    now = timezone.now()
    
    if session_key and admin_id:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE admin_sessions SET LogoutTime = %s WHERE SessionID = %s",
                [now, session_key]
            )
            
    # Clear admin keys
    request.session.pop('admin_id', None)
    request.session.pop('admin_name', None)
    request.session.pop('admin_last_activity', None)
    if request.session.get('user_role') == 'admin':
        request.session.pop('user_role', None)

def start_donor_session(request, donor_id, donor_name):
    """
    Starts a session for a donor.
    """
    request.session['donor_id'] = donor_id
    request.session['donor_name'] = donor_name
    request.session['user_role'] = 'donor'
    request.session['donor_last_activity'] = timezone.now().timestamp()

def logout_donor(request):
    """
    Logs out a donor by clearing session keys.
    """
    request.session.pop('donor_id', None)
    request.session.pop('donor_name', None)
    request.session.pop('donor_last_activity', None)
    if request.session.get('user_role') == 'donor':
        request.session.pop('user_role', None)
