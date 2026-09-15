from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
def admin_required(view_func):
    """
    Decorator for views that checks if the user is a logged-in staff administrator
    using Django's built-in authentication system.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            messages.warning(request, "Access Denied: Please log in as an administrator.")
            return redirect(f"/admin/login/?next={request.path}")
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


def recipient_required(view_func):
    """
    Decorator for views that checks if the user is a logged-in recipient.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        recipient_id = request.session.get('recipient_id')
        if not recipient_id:
            messages.warning(request, "Access Denied: Please log in to your recipient account.")
            return redirect('/DetailApp/RecipientLogin')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
