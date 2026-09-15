from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from auth_system.session_manager import start_donor_session, logout_donor, logout_recipient
from auth_system.db_helper import get_db_connection
import pymysql

def Home(request):
    total_donors = 0
    total_items = 0
    total_distributions = 0
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM donorreg")
            row = cursor.fetchone()
            if row:
                total_donors = row[0]
                
            cursor.execute("SELECT COUNT(*) FROM unusedthing")
            row = cursor.fetchone()
            if row:
                total_items = row[0]
                
            cursor.execute("SELECT COUNT(*) FROM distributetable")
            row = cursor.fetchone()
            if row:
                total_distributions = row[0]
    except Exception:
        pass

    stats = {
        'registered_users': total_donors,
        'items_donated': total_items,
        'items_redistributed': total_distributions,
    }
    return render(request, 'Home.html', {'stats': stats})

def ConnecivityPage(request):
    try:
        conn = get_db_connection()
        mycursor = conn.cursor()
        msg = "Database Connected Successfully..."
        mycursor.close()
        conn.close()
    except Exception as e:
        msg = f"Database Connection Failed: {str(e)}"
    
    return render(request, 'Connectivity.html', {'msg': msg})

def Login(request):
    if request.method == 'POST':
        login_id = (request.POST.get('userid') or request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        
        # 1. Automatic Admin Detection: Check if username/email belongs to a staff/admin user
        admin_candidate = User.objects.filter(
            Q(username__iexact=login_id) | Q(email__iexact=login_id)
        ).first()
        
        if admin_candidate and (admin_candidate.is_staff or admin_candidate.is_superuser):
            user = authenticate(request, username=admin_candidate.username, password=password)
            if user is not None and (user.is_staff or user.is_superuser):
                django_login(request, user)
                request.session['admin_id'] = user.username
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                return redirect('/admin/')
            else:
                messages.error(request, "Invalid password for Administrator account.")
                return render(request, 'LogIn.html')
        
        # 2. Donor Authentication: Check donorreg table by Donorid or Demail
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT Dpsd, Donorid, Dname FROM donorreg WHERE Donorid = %s OR Demail = %s",
                [login_id, login_id]
            )
            row = cursor.fetchone()
            
        if row:
            stored_hash, donor_id, donor_name = row
            if check_password(password, stored_hash):
                start_donor_session(request, donor_id, donor_name)
                messages.success(request, f"Welcome back, {donor_name}!")
                return redirect('/')
            else:
                messages.error(request, "Invalid password for Donor account.")
                return render(request, 'LogIn.html')
                
        messages.error(request, "Invalid User ID/Email or Password.")
        
    return render(request, 'LogIn.html')

def Logout(request):
    django_logout(request)
    logout_donor(request)
    logout_recipient(request)
    request.session.pop('admin_id', None)
    messages.info(request, "You have been logged out.")
    return redirect('/')

def Demo(request):
    return render(request, 'demo.html')

