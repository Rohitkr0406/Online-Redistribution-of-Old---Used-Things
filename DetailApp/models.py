from django.db import models

class CollectionTable(models.Model):
    slno = models.IntegerField(db_column='Slno')
    proid = models.CharField(max_length=50, primary_key=True, db_column='Proid')
    collqty = models.CharField(max_length=10, db_column='CollQty', null=True, blank=True)
    recdate = models.DateField(db_column='RecDate', null=True, blank=True)
    status = models.CharField(max_length=50, db_column='Status', null=True, blank=True)
    donby = models.CharField(max_length=100, db_column='DonBy', null=True, blank=True)
    donoradd = models.CharField(max_length=200, db_column='DonorAdd', null=True, blank=True)
    recby = models.CharField(max_length=100, db_column='RecBy', null=True, blank=True)
    remarks = models.CharField(max_length=200, db_column='Remarks', null=True, blank=True)

    class Meta:
        db_table = 'collectiontable'
        managed = False
        verbose_name = 'Collection Detail'
        verbose_name_plural = 'Collection Details'
        ordering = ['-recdate', 'slno']

    def __str__(self):
        return f"Collection {self.proid} (Donor: {self.donby})"


class StockDetails(models.Model):
    slno = models.IntegerField(db_column='Slno')
    proid = models.CharField(max_length=50, primary_key=True, db_column='Proid')
    pname = models.CharField(max_length=100, db_column='Pname', null=True, blank=True)
    cate = models.CharField(max_length=100, db_column='Cate', null=True, blank=True)
    subcate = models.CharField(max_length=100, db_column='SubCate', null=True, blank=True)
    proslno = models.CharField(max_length=100, db_column='ProSlno', null=True, blank=True)
    batchno = models.CharField(max_length=100, db_column='BatchNo', null=True, blank=True)
    disamt = models.CharField(max_length=30, db_column='DisAmt', null=True, blank=True)
    stockamt = models.CharField(max_length=30, db_column='StockAmt', null=True, blank=True)
    remarks = models.CharField(max_length=200, db_column='Remarks', null=True, blank=True)

    class Meta:
        db_table = 'stockdetails'
        managed = False
        verbose_name = 'Stock Detail'
        verbose_name_plural = 'Stock Details'
        ordering = ['slno']

    def __str__(self):
        return f"{self.pname or self.proid} (Stock: {self.stockamt})"


class DistributeTable(models.Model):
    slno = models.IntegerField(db_column='Slno')
    proid = models.CharField(max_length=50, primary_key=True, db_column='Proid')
    disqty = models.CharField(max_length=10, db_column='DisQty', null=True, blank=True)
    disdate = models.DateField(db_column='DisDate', null=True, blank=True)
    disby = models.CharField(max_length=100, db_column='DisBy', null=True, blank=True)
    recname = models.CharField(max_length=100, db_column='RecName', null=True, blank=True)
    recadd = models.CharField(max_length=200, db_column='RecAdd', null=True, blank=True)
    recmob = models.CharField(max_length=15, db_column='RecMob', null=True, blank=True)
    recby = models.CharField(max_length=100, db_column='RecBy', null=True, blank=True)
    remarks = models.CharField(max_length=200, db_column='Remarks', null=True, blank=True)

    class Meta:
        db_table = 'distributetable'
        managed = False
        verbose_name = 'Distribution Detail'
        verbose_name_plural = 'Distribution Details'
        ordering = ['-disdate', 'slno']

    def __str__(self):
        return f"Distribution {self.proid} -> {self.recname}"


class Recipient(models.Model):
    slno = models.IntegerField(null=True, blank=True, db_column='Slno')
    recipient_id = models.CharField(max_length=50, primary_key=True, db_column='Recipientid')
    name = models.CharField(max_length=100, db_column='Name')
    email = models.CharField(max_length=100, db_column='Email')
    mobile = models.CharField(max_length=20, db_column='Mobile')
    address = models.CharField(max_length=200, db_column='Address')
    city = models.CharField(max_length=50, db_column='City')
    state = models.CharField(max_length=50, db_column='State')
    pin = models.CharField(max_length=10, db_column='Pin', null=True, blank=True)
    password = models.CharField(max_length=255, db_column='Password')
    remarks = models.CharField(max_length=200, db_column='Remarks', null=True, blank=True)
    userrole = models.CharField(max_length=20, db_column='UserRole', default='recipient')
    date_joined = models.DateField(auto_now_add=True, db_column='DateJoined')

    class Meta:
        db_table = 'recipient'
        verbose_name = 'Recipient / Needy Person'
        verbose_name_plural = 'Recipients / Needy Persons'
        ordering = ['recipient_id']

    def __str__(self):
        return f"{self.name} ({self.recipient_id})"


class DonationRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Distributed', 'Distributed'),
    ]

    req_id = models.CharField(max_length=50, primary_key=True, db_column='ReqId')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, db_column='Recipientid', related_name='requests')
    item = models.ForeignKey('RegApp.UnusedThing', on_delete=models.CASCADE, db_column='Proid', db_constraint=False, related_name='requests')
    req_date = models.DateField(auto_now_add=True, db_column='ReqDate')
    status = models.CharField(max_length=30, default='Pending', choices=STATUS_CHOICES, db_column='Status')
    remarks = models.CharField(max_length=200, null=True, blank=True, db_column='Remarks')

    class Meta:
        db_table = 'donationrequest'
        verbose_name = 'Donation Request'
        verbose_name_plural = 'Donation Requests'
        ordering = ['-req_date', 'req_id']

    def __str__(self):
        return f"Request {self.req_id} [{self.status}]"
