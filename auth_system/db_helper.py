import pymysql
from django.conf import settings

def get_db_connection():
    """
    Creates and returns a connection to the MySQL database using configuration
    parameters from Django settings, which are loaded from environment variables (.env).
    """
    databases = getattr(settings, 'DATABASES', {})
    db_config = databases['default']
    return pymysql.connect(
        host=db_config.get('HOST', 'localhost'),
        user=db_config.get('USER', 'root'),
        passwd=db_config.get('PASSWORD', ''),
        db=db_config.get('NAME', ''),
        port=int(db_config.get('PORT', 3306))
    )
