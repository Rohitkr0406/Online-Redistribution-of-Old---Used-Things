import os
import sys

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinalProject.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("UPDATE unusedthing SET Donorid = 'donor1' WHERE Donorid IS NULL")
    print("Database updated successfully!")
