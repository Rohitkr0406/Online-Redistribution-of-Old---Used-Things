# Admin Panel Implementation Task

## Objective
Implement a complete Admin Panel with authentication, role-based access control, and admin-only features for the "Online Redistribution of Old & Used Things" application.

## Current State Analysis
- **Problem**: The application currently has no admin panel or role-based access control
- **Reports visibility**: All reports are publicly accessible without authentication
- **Missing**: Admin login, admin dashboard, session management, role differentiation

---

## Requirements to Implement

### 1. Admin Authentication Module
**Location**: Create `AdminApp/` directory with authentication

#### Files to create:
- `AdminApp/models.py` - Admin user model
- `AdminApp/views.py` - Admin login/logout views
- `AdminApp/urls.py` - URL routing for admin

#### Requirements:
```
✓ Create Admin registration/login page
✓ Admin credentials stored securely (password hashing using Django's make_password)
✓ Admin login form with email/username and password
✓ Session management using Django sessions
✓ "Remember Me" functionality (optional)
✓ Admin logout functionality
✓ Admin login should NOT interfere with donor login
✓ Both admin and donor can access simultaneously
```

#### Database Table:
Create `adminlogin` table:
```sql
- AdminID (Primary Key)
- AdminName
- AdminEmail
- AdminPassword (hashed)
- AdminPhone
- AdminAddress
- Created_Date
- Status (Active/Inactive)
```

---

### 2. Session & Authentication Management
**Location**: Middleware and authentication utilities

#### Requirements:
```
✓ Session creation on admin login
✓ Session validation for admin-only views
✓ Admin session timeout (30 minutes)
✓ Admin can't access donor-only pages
✓ Donor can't access admin-only pages
✓ Create authentication decorator @admin_required
✓ Create authentication decorator @donor_required
✓ Maintain separate session keys for admin vs donor
```

#### Implementation:
- Create `middleware/auth_middleware.py` - Custom authentication middleware
- Create `decorators/auth_decorators.py` - @admin_required and @donor_required decorators
- Create `utils/session_manager.py` - Session handling utilities

---

### 3. Admin Dashboard
**Location**: `AdminApp/views.py` and `templates/AdminDashboard.html`

#### Dashboard Features:
```
✓ Welcome section with admin name
✓ Quick stats:
  - Total Donors
  - Total Items Donated
  - Total Requests Received
  - Items in Stock
  - Items Distributed
  - Pending Distributions
  - Total Complaints

✓ Recent activities (last 5):
  - Recent donations
  - Recent requests
  - Recent distributions
  - Recent complaints

✓ Navigation menu to all admin modules:
  - Donor Management
  - Items Management
  - Collection Management
  - Stock Management
  - Distribution Management
  - Report Generation
  - Complaint Management
  - User Feedback
  - Admin Settings
```

#### Implementation:
```python
def AdminDashboard(request):
    # Check if admin is logged in using @admin_required
    # Calculate and display statistics
    # Fetch recent activities
    # Return dashboard template with data
```

---

### 4. Admin-Only Report Access
**Location**: Modify `ReportApp/views.py`

#### Current Issue:
Reports are accessible without login

#### Fix Required:
```python
# Add @admin_required decorator to all report views:
@admin_required
def DonorReport(request):
    # Existing code
    pass

@admin_required
def UnusedReport(request):
    # Existing code
    pass

@admin_required
def CollectionReport(request):
    # Existing code
    pass

@admin_required
def StockReport(request):
    # Existing code
    pass

@admin_required
def DistributionReport(request):
    # Existing code
    pass

@admin_required
def ComplaintReport(request):
    # Existing code
    pass

@admin_required
def ContactUsReport(request):
    # Existing code
    pass
```

---

### 5. Admin-Only Data Management Pages
**Location**: Modify `DetailApp/views.py` and `RegApp/views.py`

#### Current Issue:
Collection, Stock, Distribution, and Donor Management are accessible without login

#### Fix Required:
```python
# Add @admin_required to all admin operations:

@admin_required
def Collection(request):
    pass

@admin_required
def CollectionSave(request):
    pass

@admin_required
def Stock(request):
    pass

@admin_required
def StockSave(request):
    pass

@admin_required
def Distribution(request):
    pass

@admin_required
def DistributionSave(request):
    pass

@admin_required
def Donator(request):  # Donor Management
    pass
```

---

### 6. Role-Based Access Control (RBAC)
**Location**: Create `auth_system/` with RBAC logic

#### User Roles:
```
ROLES:
- Admin (Full access to all features)
- Donor (Can register, list items, view own donations)
- Receiver (Can view available items, make requests)
```

#### Access Matrix:
```
                    Admin    Donor    Receiver
Dashboard           ✓        ✗        ✗
All Reports         ✓        ✗        ✗
Manage Donors       ✓        ✗        ✗
Manage Items        ✓        ✓*       ✗*
Collection          ✓        ✗        ✗
Stock               ✓        ✗        ✗
Distribution        ✓        ✗        ✗
View Complaints     ✓        ✓(own)   ✓(own)
Home Page           ✓        ✓        ✓
Login               ✓        ✓        ✓

* Donors can only manage their own items
```

---

### 7. Login Flow Integration
**Location**: Modify `FirstApp/views.py` and create `templates/LogIn.html`

#### Current Issue:
Single login page doesn't differentiate between admin and donor

#### Fix Required:
```python
def Login(request):
    if request.method == 'GET':
        return render(request, 'LogIn.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # 'admin' or 'donor'
        
        if user_type == 'admin':
            # Check admin credentials
            # Create admin session
            # Redirect to AdminDashboard
        else:
            # Check donor credentials
            # Create donor session
            # Redirect to DonorHome
```

---

### 8. Database Changes
**SQL Migrations Required**:

```sql
-- Create Admin Login Table
CREATE TABLE adminlogin (
    AdminID VARCHAR(50) PRIMARY KEY,
    AdminName VARCHAR(100) NOT NULL,
    AdminEmail VARCHAR(100) NOT NULL UNIQUE,
    AdminPassword VARCHAR(255) NOT NULL,
    AdminPhone VARCHAR(15),
    AdminAddress VARCHAR(255),
    Created_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status VARCHAR(20) DEFAULT 'Active'
);

-- Add role column to donor table (optional, for future use)
ALTER TABLE donorreg ADD COLUMN UserRole VARCHAR(20) DEFAULT 'donor';

-- Add session tracking table (optional)
CREATE TABLE admin_sessions (
    SessionID VARCHAR(100) PRIMARY KEY,
    AdminID VARCHAR(50),
    LoginTime DATETIME,
    LastActivity DATETIME,
    LogoutTime DATETIME,
    FOREIGN KEY (AdminID) REFERENCES adminlogin(AdminID)
);
```

---

### 9. Security Requirements
```
✓ Hash admin passwords using Django's make_password (PBKDF2)
✓ Implement CSRF protection on all forms
✓ Validate all inputs (sanitize)
✓ Use secure session cookies (HttpOnly, Secure flags)
✓ Implement rate limiting on login attempts
✓ Log all admin actions (for audit trail)
✓ No sensitive data in logs
✓ Admin operations should NOT be visible to donors
```

---

### 10. File Structure to Create

```
AdminApp/
├── __init__.py
├── models.py
├── views.py
├── urls.py
├── forms.py
└── admin_utils.py

auth_system/
├── __init__.py
├── decorators.py
├── session_manager.py
└── middleware.py

templates/
├── AdminLogIn.html          (NEW)
├── AdminDashboard.html      (NEW)
├── AdminMenu.html           (NEW - included in all admin pages)
└── [modify existing reports]

static/
└── css/
    └── admin_dashboard.css  (NEW)
```

---

### 11. Templates to Create/Modify

#### New Templates:
```
1. AdminLogIn.html
   - Admin login form
   - Username/Email and Password fields
   - "Login as Admin" button
   - Link to switch to Donor login

2. AdminDashboard.html
   - Welcome banner with admin name
   - Statistics cards (6 cards with metrics)
   - Recent activities table
   - Main navigation menu

3. AdminMenu.html
   - Side/Top navigation menu
   - Links to all admin modules
   - Logout button
   - Admin profile link

4. AdminSettings.html
   - Change admin password
   - Update admin profile
   - View admin audit logs
```

#### Modify:
```
1. LogIn.html
   - Add radio buttons to select User Type (Admin/Donor)
   - Show appropriate login form based on selection
   - Different login endpoints for admin/donor

2. Home.html
   - Add condition: if admin logged in, show admin dashboard
   - If donor logged in, show donor home
   - If not logged in, show public home
```

---

### 12. URL Routing
**Location**: `FinalProject/urls.py` and create `AdminApp/urls.py`

#### New URL Patterns:
```python
path('admin/login/', views.AdminLogin, name='admin_login'),
path('admin/dashboard/', views.AdminDashboard, name='admin_dashboard'),
path('admin/logout/', views.AdminLogout, name='admin_logout'),
path('admin/donors/', views.AdminDonorManagement, name='admin_donors'),
path('admin/items/', views.AdminItemsManagement, name='admin_items'),
path('admin/settings/', views.AdminSettings, name='admin_settings'),

# Existing URLs should be preserved but now with @admin_required
path('reports/donor/', views.DonorReport, name='donor_report'),
path('reports/items/', views.UnusedReport, name='unused_report'),
```

---

### 13. Testing Checklist
```
□ Admin login with correct credentials works
□ Admin login with incorrect credentials fails
□ Admin dashboard loads after login
□ Admin can access all reports
□ Donor cannot access admin dashboard
□ Donor cannot access admin reports
□ Admin can access collection/stock/distribution pages
□ Donor cannot access collection/stock/distribution pages
□ Session timeout after 30 minutes
□ Logout clears session properly
□ Both admin and donor can be logged in simultaneously (different browsers)
□ All admin operations log their activity
□ CSRF protection works
□ Rate limiting on login attempts works
□ Navigation menu appears only for logged-in admins
```

---

### 14. Implementation Steps (In Order)
1. Create `AdminApp` directory structure
2. Create `adminlogin` database table
3. Implement Admin models in `AdminApp/models.py`
4. Create authentication decorators (`@admin_required`, `@donor_required`)
5. Implement Admin login view and template
6. Create session management utilities
7. Create Admin dashboard view and template
8. Add `@admin_required` decorators to all report views
9. Add `@admin_required` decorators to all admin-only views
10. Modify Login page to support both admin and donor
11. Create Admin menu/navigation template
12. Create Admin settings page
13. Test all scenarios from Testing Checklist
14. Add error pages (403 Forbidden, etc.)
15. Document admin credentials and login process

---

### 15. Additional Notes
- Keep donor login functionality exactly as is
- Do NOT break existing donor features
- Admin and donor sessions must be separate
- Admin operations must not appear in donor dashboard
- Password should be encrypted in database
- Create a default admin user in migration script
- Default admin credentials: (Username: `admin`, Password: `admin123` - change on first login)
- All timestamps should be in consistent format
- Use Django's built-in admin features where applicable

---

## Deliverables
1. ✓ Separate Admin login page and functionality
2. ✓ Admin dashboard with statistics
3. ✓ Role-based access control for all pages
4. ✓ Admin-only report access
5. ✓ Admin-only data management pages
6. ✓ Session management system
7. ✓ Authentication decorators
8. ✓ Database table for admin users
9. ✓ Updated URL routing
10. ✓ Error handling for unauthorized access
11. ✓ Audit logging for admin actions
12. ✓ All tests passing

---

## Success Criteria
- [ ] Admin can log in with separate credentials
- [ ] Admin dashboard displays statistics
- [ ] Reports are only visible to logged-in admins
- [ ] Donors cannot access admin pages
- [ ] All admin operations are restricted by role
- [ ] Session management works correctly
- [ ] No security vulnerabilities
- [ ] Application performance is not degraded

