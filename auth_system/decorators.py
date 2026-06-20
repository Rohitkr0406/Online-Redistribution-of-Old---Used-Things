from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from .session_manager import logout_admin, update_admin_activity

def admin_required(view_func):
    """
    Decorator for views that checks if the user is a logged-in admin.
    Also handles the 30-minute session inactivity timeout.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        admin_id = request.session.get('admin_id')
        if not admin_id:
            messages.warning(request, "Access Denied: Please log in as an administrator.")
            return redirect('admin_login')
        
        # Check timeout
        last_activity = request.session.get('admin_last_activity')
        now = timezone.now().timestamp()
        
        if last_activity:
            elapsed_time = now - last_activity
            if elapsed_time > 1800:  # 30 minutes = 1800 seconds
                logout_admin(request)
                messages.warning(request, "Session Expired: You have been logged out due to inactivity.")
                return redirect('admin_login')
        
        # Update activity timestamp
        update_admin_activity(request)
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def donor_required(view_func):
    """
    Decorator for views that checks if the user is a logged-in donor.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        donor_id = request.session.get('donor_id')
        if not donor_id:
            messages.warning(request, "Access Denied: Please log in to your donor account.")
            return redirect('/FirstApp/Login')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
