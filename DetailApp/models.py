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
