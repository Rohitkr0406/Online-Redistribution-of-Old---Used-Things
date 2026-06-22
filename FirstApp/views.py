from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from auth_system.session_manager import start_admin_session, start_donor_session, logout_donor
from auth_system.db_helper import get_db_connection
import pymysql

def Home(request):
    return render(request, 'Home.html')

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
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT AdminID, AdminName, AdminPassword, Status FROM adminlogin WHERE AdminID = %s OR AdminEmail = %s",
                    [username, username]
                )
                row = cursor.fetchone()
                
            if row:
                admin_id, admin_name, hashed_pw, status = row[0], row[1], row[2], row[3]
                if status != 'Active':
                    messages.error(request, "Account Inactive: Your administrator account has been deactivated.")
                    return render(request, 'LogIn.html')
                    
                if check_password(password, hashed_pw):
                    start_admin_session(request, admin_id, admin_name)
                    from AdminApp.admin_utils import log_admin_action
                    log_admin_action(admin_id, "Login", "Admin logged in via unified login page.")
                    messages.success(request, f"Welcome back, {admin_name}!")
                    return redirect('admin_dashboard')
            
            messages.error(request, "Invalid Admin credentials.")
            
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
    logout_donor(request)
    messages.info(request, "You have been logged out.")
    return redirect('/')

def Demo(request):
    return render(request, 'demo.html')

