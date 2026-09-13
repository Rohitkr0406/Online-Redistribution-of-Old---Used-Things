from django.db import models

class ComplaintTable(models.Model):
    slno = models.IntegerField(db_column='Slno')
    did = models.CharField(max_length=50, primary_key=True, db_column='Did')
    compdate = models.DateField(db_column='CompDate', null=True, blank=True)
    issutype = models.CharField(max_length=50, db_column='IssuType', null=True, blank=True)
    compdetails = models.CharField(max_length=500, db_column='CompDetails', null=True, blank=True)
    remarks = models.CharField(max_length=200, db_column='Remarks', null=True, blank=True)

    class Meta:
        db_table = 'complainttable'
        managed = False
        verbose_name = 'Complaint & Suggestion'
        verbose_name_plural = 'Complaints & Suggestions'
        ordering = ['-compdate', 'slno']

    def __str__(self):
        return f"Complaint by {self.did} ({self.issutype})"


class ContactUs(models.Model):
    slno = models.IntegerField(db_column='Slno')
    admid = models.CharField(max_length=50, primary_key=True, db_column='Admid')
    comname = models.CharField(max_length=50, db_column='ComName', null=True, blank=True)
    comemail = models.CharField(max_length=50, db_column='ComEmail', null=True, blank=True)
    comadd = models.CharField(max_length=200, db_column='ComAdd', null=True, blank=True)
    commob = models.CharField(max_length=50, db_column='ComMob', null=True, blank=True)
    remarks = models.CharField(max_length=200, db_column='Remarks', null=True, blank=True)

    class Meta:
        db_table = 'contactus'
        managed = False
        verbose_name = 'Contact Us Entry'
        verbose_name_plural = 'Contact Us Entries'
        ordering = ['slno']

    def __str__(self):
        return f"{self.comname} ({self.comemail})"
