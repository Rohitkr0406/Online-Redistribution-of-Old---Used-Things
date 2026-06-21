from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from auth_system.decorators import admin_required
from auth_system.session_manager import start_admin_session, logout_admin
from AdminApp.admin_utils import log_admin_action
from AdminApp.forms import ChangePasswordForm

def AdminLogin(request):
    """
    Renders admin login form and processes credentials.
    """
    if request.session.get('admin_id'):
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT AdminID, AdminName, AdminEmail, AdminPassword, Status FROM adminlogin WHERE AdminID = %s OR AdminEmail = %s",
                [username, username]
            )
            row = cursor.fetchone()
            
        if row:
            admin_id, admin_name, admin_email, hashed_pw, status = row
            if status != 'Active':
                messages.error(request, "Account Inactive: Your administrator account has been deactivated.")
                return render(request, 'AdminLogIn.html')
                
            if check_password(password, hashed_pw):
                start_admin_session(request, admin_id, admin_name)
                log_admin_action(admin_id, "Login", "Admin logged in successfully.")
                messages.success(request, f"Welcome back, {admin_name}!")
                return redirect('admin_dashboard')
            
        messages.error(request, "Invalid credentials. Please verify username/email and password.")
        
    return render(request, 'AdminLogIn.html')

def AdminLogout(request):
    """
    Logs out the admin and destroys the session.
    """
    admin_id = request.session.get('admin_id')
    if admin_id:
        log_admin_action(admin_id, "Logout", "Admin logged out.")
    logout_admin(request)
    messages.info(request, "You have been logged out.")
    return redirect('admin_login')

@admin_required
def AdminDashboard(request):
    """
    Fetches statistics and recent records to display on the Admin Dashboard.
    """
    admin_name = request.session.get('admin_name')
    
    # Calculate stats
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM donorreg")
        total_donors = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM unusedthing")
        total_items = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM distributetable")
        total_requests = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(CAST(StockAmt AS SIGNED)) FROM stockdetails")
        stock_sum = cursor.fetchone()[0]
        items_in_stock = stock_sum if stock_sum is not None else 0
        
        cursor.execute("SELECT SUM(CAST(DisAmt AS SIGNED)) FROM stockdetails")
        dis_sum = cursor.fetchone()[0]
        items_distributed = dis_sum if dis_sum is not None else 0
        
        cursor.execute("SELECT COUNT(*) FROM stockdetails WHERE CAST(StockAmt AS SIGNED) > 0")
        pending_distributions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM complainttable")
        total_complaints = cursor.fetchone()[0]
        
    stats = {
        'total_donors': total_donors,
        'total_items': total_items,
        'total_requests': total_requests,
        'items_in_stock': items_in_stock,
        'items_distributed': items_distributed,
        'pending_distributions': pending_distributions,
        'total_complaints': total_complaints,
    }
    
    # Fetch recent activities (last 5)
    with connection.cursor() as cursor:
        cursor.execute("SELECT Slno, Proid, ProName, ProCate, Status FROM unusedthing ORDER BY Slno DESC LIMIT 5")
        recent_donations = cursor.fetchall()
        
        cursor.execute("SELECT Slno, Proid, DisQty, DisDate, RecName FROM distributetable ORDER BY Slno DESC LIMIT 5")
        recent_distributions = cursor.fetchall()
        
        cursor.execute("SELECT Slno, Did, CompDate, IssuType, CompDetails FROM complainttable ORDER BY Slno DESC LIMIT 5")
        recent_complaints = cursor.fetchall()
        
        cursor.execute("SELECT Slno, ComName, ComEmail, ComMob, Remarks FROM contactus ORDER BY Slno DESC LIMIT 5")
        recent_feedbacks = cursor.fetchall()
        
    recent_activities = {
        'recent_donations': recent_donations,
        'recent_distributions': recent_distributions,
        'recent_complaints': recent_complaints,
        'recent_feedbacks': recent_feedbacks,
    }
    
    context = {
        'admin_name': admin_name,
        'stats': stats,
        'recent': recent_activities
    }
    return render(request, 'AdminDashboard.html', context)

@admin_required
def AdminDonorManagement(request):
    """
    Allows admin to list and search donors.
    """
    search_query = request.GET.get('search', '')
    donors = []
    
    with connection.cursor() as cursor:
        if search_query:
            cursor.execute(
                "SELECT Slno, Donorid, Dname, Demail, Dmob, City, State, Status FROM donorreg WHERE Donorid LIKE %s OR Dname LIKE %s OR Demail LIKE %s OR City LIKE %s",
                [f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"]
            )
        else:
            cursor.execute("SELECT Slno, Donorid, Dname, Demail, Dmob, City, State, 'Active' FROM donorreg")
        donors = cursor.fetchall()
        
    return render(request, 'AdminDonors.html', {'donors': donors, 'search_query': search_query})

@admin_required
def AdminItemsManagement(request):
    """
    Allows admin to view all registered items.
    """
    search_query = request.GET.get('search', '')
    items = []
    
    with connection.cursor() as cursor:
        if search_query:
            cursor.execute(
                "SELECT Slno, Proid, ProName, ProCate, ProSubCate, Status, Remarks FROM unusedthing WHERE Proid LIKE %s OR ProName LIKE %s OR ProCate LIKE %s",
                [f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"]
            )
        else:
            cursor.execute("SELECT Slno, Proid, ProName, ProCate, ProSubCate, Status, Remarks FROM unusedthing")
        items = cursor.fetchall()
        
    return render(request, 'AdminItems.html', {'items': items, 'search_query': search_query})

@admin_required
def AdminSettings(request):
    """
    Admin profile update, password change, and audit log viewer.
    """
    admin_id = request.session.get('admin_id')
    form = ChangePasswordForm()
    
    # Process POST actions
    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        
        if action_type == 'change_password':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']
                
                with connection.cursor() as cursor:
                    cursor.execute("SELECT AdminPassword FROM adminlogin WHERE AdminID = %s", [admin_id])
                    row = cursor.fetchone()
                    
                if row and check_password(old_password, row[0]):
                    hashed_pw = make_password(new_password)
                    with connection.cursor() as cursor:
                        cursor.execute("UPDATE adminlogin SET AdminPassword = %s WHERE AdminID = %s", [hashed_pw, admin_id])
                    log_admin_action(admin_id, "Change Password", "Admin changed password successfully.")
                    messages.success(request, "Password updated successfully!")
                    return redirect('admin_settings')
                else:
                    messages.error(request, "Failed to change password: Current password is incorrect.")
            else:
                for error in form.non_field_errors():
                    messages.error(request, error)
                    
        elif action_type == 'update_profile':
            admin_name = request.POST.get('admin_name')
            admin_phone = request.POST.get('admin_phone')
            admin_address = request.POST.get('admin_address')
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE adminlogin SET AdminName = %s, AdminPhone = %s, AdminAddress = %s WHERE AdminID = %s",
                    [admin_name, admin_phone, admin_address, admin_id]
                )
            request.session['admin_name'] = admin_name
            log_admin_action(admin_id, "Update Profile", f"Profile details updated: Phone={admin_phone}, Address={admin_address}")
            messages.success(request, "Profile updated successfully!")
            return redirect('admin_settings')
            
    # Fetch admin profile data
    with connection.cursor() as cursor:
        cursor.execute("SELECT AdminID, AdminName, AdminEmail, AdminPhone, AdminAddress, Created_Date FROM adminlogin WHERE AdminID = %s", [admin_id])
        profile = cursor.fetchone()
        
    # Fetch audit logs (last 50)
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT LogID, Action, Details, Timestamp FROM admin_audit_logs WHERE AdminID = %s ORDER BY Timestamp DESC LIMIT 50",
            [admin_id]
        )
        audit_logs = cursor.fetchall()
        
    context = {
        'profile': {
            'id': profile[0],
            'name': profile[1],
            'email': profile[2],
            'phone': profile[3],
            'address': profile[4],
            'created_date': profile[5],
        },
        'form': form,
        'audit_logs': audit_logs
    }
    return render(request, 'AdminSettings.html', context)

@admin_required
def AdminApproveItem(request):
    """
    Allows admin to approve or reject a donated item.
    Updates the Status field in the unusedthing table.
    """
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')  # 'Approved' or 'Rejected'
        admin_id = request.session.get('admin_id')
        
        if item_id and action in ['Approved', 'Rejected']:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE unusedthing SET Status = %s WHERE Proid = %s",
                    [action, item_id]
                )
            log_admin_action(
                admin_id, 
                f"Item {action}", 
                f"Item Proid={item_id} has been {action.lower()} by admin."
            )
            messages.success(request, f"Item {item_id} has been {action.lower()} successfully.")
        else:
            messages.error(request, "Invalid action or item ID.")
    
    return redirect('admin_items')
