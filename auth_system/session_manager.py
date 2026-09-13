from django.utils import timezone

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
