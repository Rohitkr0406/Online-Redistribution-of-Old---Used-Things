from django.db import models

class DonorReg(models.Model):
    slno = models.IntegerField(db_column='Slno')
    donorid = models.CharField(max_length=50, primary_key=True, db_column='Donorid')
    dname = models.CharField(max_length=100, db_column='Dname', null=True, blank=True)
    dpsd = models.CharField(max_length=255, db_column='Dpsd')
    dcpsd = models.CharField(max_length=255, db_column='Dcpsd')
    dob = models.DateField(db_column='Dob', null=True, blank=True)
    gen = models.CharField(max_length=20, db_column='Gen', null=True, blank=True)
    dmob = models.CharField(max_length=15, db_column='Dmob', null=True, blank=True)
    demail = models.CharField(max_length=100, db_column='Demail', null=True, blank=True)
    add1 = models.CharField(max_length=100, db_column='Add1', null=True, blank=True)
    add2 = models.CharField(max_length=100, db_column='Add2', null=True, blank=True)
    state = models.CharField(max_length=50, db_column='State', null=True, blank=True)
    city = models.CharField(max_length=50, db_column='City', null=True, blank=True)
    pin = models.CharField(max_length=10, db_column='Pin', null=True, blank=True)
    remarks = models.CharField(max_length=200, db_column='Remarks', null=True, blank=True)
    userrole = models.CharField(max_length=20, db_column='UserRole', null=True, blank=True, default='donor')

    class Meta:
        db_table = 'donorreg'
        managed = False
        verbose_name = 'Donor'
        verbose_name_plural = 'Donors'
        ordering = ['slno']

    def __str__(self):
        return f"{self.dname or self.donorid} ({self.donorid})"


class UnusedThing(models.Model):
    slno = models.IntegerField(db_column='Slno')
    proid = models.CharField(max_length=50, primary_key=True, db_column='Proid')
    proname = models.CharField(max_length=100, db_column='ProName', null=True, blank=True)
    procate = models.CharField(max_length=100, db_column='ProCate', null=True, blank=True)
    prosubcate = models.CharField(max_length=100, db_column='ProSubCate', null=True, blank=True)
    proserial = models.CharField(max_length=100, db_column='ProSerial', null=True, blank=True)
    probatchno = models.CharField(max_length=100, db_column='ProBatchno', null=True, blank=True)
    purchdate = models.DateField(db_column='PurchDate', null=True, blank=True)
    status = models.CharField(max_length=50, db_column='Status', null=True, blank=True)
    remarks = models.CharField(max_length=200, db_column='Remarks', null=True, blank=True)
    donorid = models.CharField(max_length=50, db_column='Donorid', null=True, blank=True)

    class Meta:
        db_table = 'unusedthing'
        managed = False
        verbose_name = 'Unused Thing / Donation'
        verbose_name_plural = 'Unused Things / Donations'
        ordering = ['-purchdate', 'slno']

    def __str__(self):
        return f"{self.proname or self.proid} ({self.proid})"
