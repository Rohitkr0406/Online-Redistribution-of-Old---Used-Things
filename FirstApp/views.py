from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.hashers import check_password
from auth_system.session_manager import start_donor_session, logout_donor
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
        username = request.POST.get('userid') or request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # 'admin' or 'donor'
        
        if user_type == 'admin':
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                django_login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                return redirect('/admin/')
            messages.error(request, "Invalid Admin credentials or unauthorized staff account.")
            
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT Dpsd, Donorid, Dname FROM donorreg WHERE Donorid = %s OR Demail = %s",
                    [username, username]
                )
                row = cursor.fetchone()
                
            if row:
                stored_hash, donor_id, donor_name = row
                if check_password(password, stored_hash):
                    start_donor_session(request, donor_id, donor_name)
                    messages.success(request, f"Welcome back, {donor_name}!")
                    return redirect('/')
                    
            messages.error(request, "Invalid Donor ID or Password.")
            
    return render(request, 'LogIn.html')

def Logout(request):
    django_logout(request)
    logout_donor(request)
    messages.info(request, "You have been logged out.")
    return redirect('/')

def Demo(request):
    return render(request, 'demo.html')

