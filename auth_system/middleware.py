from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from auth_system.session_manager import logout_admin

class AdminSessionMiddleware:
    """
    Middleware to globally enforce admin authentication and session timeout
    on all URLs starting with '/admin/' (excluding the login page itself).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        # Check if the path targets the custom admin panel (excluding login)
        if path.startswith('/admin/') and not path.startswith('/admin/login/'):
            admin_id = request.session.get('admin_id')
            if not admin_id:
                messages.warning(request, "Access Denied: Please log in as an administrator.")
                return redirect('admin_login')
            
            # Check inactivity timeout
            last_activity = request.session.get('admin_last_activity')
            now = timezone.now().timestamp()
            
            if last_activity:
                elapsed_time = now - last_activity
                if elapsed_time > 1800:  # 30 minutes
                    logout_admin(request)
                    messages.warning(request, "Session Expired: You have been logged out due to inactivity.")
                    return redirect('admin_login')
            
            # Note: We let views update the last activity or update it here
            request.session['admin_last_activity'] = now
            
        response = self.get_response(request)
        return response
