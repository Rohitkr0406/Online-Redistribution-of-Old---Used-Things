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

def start_recipient_session(request, recipient_id, recipient_name):
    """
    Starts a session for a recipient.
    """
    request.session['recipient_id'] = recipient_id
    request.session['recipient_name'] = recipient_name
    request.session['user_role'] = 'recipient'
    request.session['recipient_last_activity'] = timezone.now().timestamp()

def logout_recipient(request):
    """
    Logs out a recipient by clearing session keys.
    """
    request.session.pop('recipient_id', None)
    request.session.pop('recipient_name', None)
    request.session.pop('recipient_last_activity', None)
    if request.session.get('user_role') == 'recipient':
        request.session.pop('user_role', None)
