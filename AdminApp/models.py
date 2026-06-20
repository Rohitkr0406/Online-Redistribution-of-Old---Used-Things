from django.db import models

class AdminLogin(models.Model):
    AdminID = models.CharField(max_length=50, primary_key=True)
    AdminName = models.CharField(max_length=100)
    AdminEmail = models.EmailField(max_length=100, unique=True)
    AdminPassword = models.CharField(max_length=255)
    AdminPhone = models.CharField(max_length=15, null=True, blank=True)
    AdminAddress = models.CharField(max_length=255, null=True, blank=True)
    Created_Date = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=20, default='Active')

    class Meta:
        db_table = 'adminlogin'

    def __str__(self):
        return f"{self.AdminName} ({self.AdminID})"


class AdminSessions(models.Model):
    SessionID = models.CharField(max_length=100, primary_key=True)
    Admin = models.ForeignKey(AdminLogin, on_delete=models.CASCADE, db_column='AdminID')
    LoginTime = models.DateTimeField(null=True, blank=True)
    LastActivity = models.DateTimeField(null=True, blank=True)
    LogoutTime = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'admin_sessions'


class AdminAuditLog(models.Model):
    LogID = models.AutoField(primary_key=True)
    Admin = models.ForeignKey(AdminLogin, on_delete=models.CASCADE, db_column='AdminID')
    Action = models.CharField(max_length=255)
    Details = models.TextField(null=True, blank=True)
    Timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_audit_logs'
