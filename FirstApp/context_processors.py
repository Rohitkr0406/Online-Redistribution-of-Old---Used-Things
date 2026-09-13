import os

def project_settings(request):
    """
    Context processor to provide global settings such as contact phone to all templates.
    """
    return {
        'contact_phone': os.getenv('CONTACT_PHONE', '+91 7992241733'),
    }
