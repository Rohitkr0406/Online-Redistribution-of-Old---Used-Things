import pymysql
from django.shortcuts import render

def get_db_connection():
    return pymysql.connect(host='localhost', user='root', passwd='destroyer3607', db='stud')

def ReportHome(request):
    return render(request, 'Report.html')

# --- DONOR REPORT ---
def DonorReport(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM donorreg ORDER BY Slno")
    record1 = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return render(request, 'DonorReport.html', {'record1': record1, 'record2': None})

def DonorReportSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM donorreg ORDER BY Slno")
    record1 = mycursor.fetchall()
    
    CmbBox = request.POST.get('CmbBox')
    if CmbBox and CmbBox != "All" and CmbBox != "-Select-":
        mycursor.execute("SELECT * FROM donorreg WHERE Slno = %s ORDER BY Slno", (CmbBox,))
        record2 = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM donorreg ORDER BY Slno")
        record2 = mycursor.fetchall()
        
    mycursor.close()
    conn.close()
    return render(request, 'DonorReport.html', {'record1': record1, 'record2': record2})

# --- UNUSED REPORT ---
def UnusedReport(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM unusedthing ORDER BY Slno")
    record1 = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return render(request, 'UnUsedReport.html', {'record1': record1, 'record2': None})

def UnusedReportSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM unusedthing ORDER BY Slno")
    record1 = mycursor.fetchall()
    
    CmbBox = request.POST.get('CmbBox')
    if CmbBox and CmbBox != "All" and CmbBox != "-Select-":
        mycursor.execute("SELECT * FROM unusedthing WHERE Slno = %s ORDER BY Slno", (CmbBox,))
        record2 = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM unusedthing ORDER BY Slno")
        record2 = mycursor.fetchall()
        
    mycursor.close()
    conn.close()
    return render(request, 'UnUsedReport.html', {'record1': record1, 'record2': record2})

# --- COLLECTION REPORT ---
def CollectionReport(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT DISTINCT Proid FROM collectiontable ORDER BY Proid")
    record1 = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return render(request, 'CollectionReport.html', {'record1': record1, 'record2': None, 'record3': None})

def CollectionReportSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT DISTINCT Proid FROM collectiontable ORDER BY Proid")
    record1 = mycursor.fetchall()
    
    CmbBox = request.POST.get('CmbBox')
    if CmbBox and CmbBox != "All" and CmbBox != "-Select-":
        mycursor.execute("""
            SELECT c.Slno, c.Proid, u.ProName, u.ProCate, u.ProSubCate, u.ProSerial, u.ProBatchno, 
                   c.CollQty, c.RecDate, c.Status, c.DonBy, c.DonorAdd, c.RecBy, c.Remarks 
            FROM collectiontable c 
            LEFT JOIN unusedthing u ON c.Proid = u.Proid 
            WHERE c.Proid = %s
        """, (CmbBox,))
        record2 = mycursor.fetchall()
    else:
        mycursor.execute("""
            SELECT c.Slno, c.Proid, u.ProName, u.ProCate, u.ProSubCate, u.ProSerial, u.ProBatchno, 
                   c.CollQty, c.RecDate, c.Status, c.DonBy, c.DonorAdd, c.RecBy, c.Remarks 
            FROM collectiontable c 
            LEFT JOIN unusedthing u ON c.Proid = u.Proid 
            ORDER BY c.Slno
        """)
        record2 = mycursor.fetchall()
        
    mycursor.close()
    conn.close()
    return render(request, 'CollectionReport.html', {'record1': record1, 'record2': record2})

# --- STOCK REPORT ---
def StockReport(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM stockdetails ORDER BY Slno")
    record1 = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return render(request, 'StockReport.html', {'record1': record1, 'record2': None})

def StockReportSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM stockdetails ORDER BY Slno")
    record1 = mycursor.fetchall()
    
    CmbBox = request.POST.get('CmbBox')
    if CmbBox and CmbBox != "All" and CmbBox != "-Select-":
        mycursor.execute("SELECT * FROM stockdetails WHERE Slno = %s ORDER BY Slno", (CmbBox,))
        record2 = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM stockdetails ORDER BY Slno")
        record2 = mycursor.fetchall()
        
    mycursor.close()
    conn.close()
    return render(request, 'StockReport.html', {'record1': record1, 'record2': record2})

# --- DISTRIBUTION REPORT ---
def DistributionReport(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM distributetable ORDER BY Slno")
    record1 = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return render(request, 'DistributionReport.html', {'record1': record1, 'record2': None})

def DistributionReportSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM distributetable ORDER BY Slno")
    record1 = mycursor.fetchall()
    
    CmbBox = request.POST.get('CmbBox')
    if CmbBox and CmbBox != "All" and CmbBox != "-Select-":
        mycursor.execute("""
            SELECT d.Slno, d.Proid, u.ProName, u.ProCate, u.ProSubCate, u.ProSerial, u.ProBatchno, 
                   d.DisQty, d.DisDate, d.DisBy, d.RecName, d.RecAdd, d.RecMob, d.RecBy, d.Remarks 
            FROM distributetable d 
            LEFT JOIN unusedthing u ON d.Proid = u.Proid 
            WHERE d.Slno = %s 
            ORDER BY d.Slno
        """, (CmbBox,))
        record2 = mycursor.fetchall()
    else:
        mycursor.execute("""
            SELECT d.Slno, d.Proid, u.ProName, u.ProCate, u.ProSubCate, u.ProSerial, u.ProBatchno, 
                   d.DisQty, d.DisDate, d.DisBy, d.RecName, d.RecAdd, d.RecMob, d.RecBy, d.Remarks 
            FROM distributetable d 
            LEFT JOIN unusedthing u ON d.Proid = u.Proid 
            ORDER BY d.Slno
        """)
        record2 = mycursor.fetchall()
        
    mycursor.close()
    conn.close()
    return render(request, 'DistributionReport.html', {'record1': record1, 'record2': record2})

# --- COMPLAINT REPORT ---
def ComplaintReport(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM complainttable ORDER BY Slno")
    record1 = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return render(request, 'ComplaintReport.html', {'record1': record1, 'record2': None})

def ComplaintReportSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM complainttable ORDER BY Slno")
    record1 = mycursor.fetchall()
    
    CmbBox = request.POST.get('CmbBox')
    if CmbBox and CmbBox != "All" and CmbBox != "-Select-":
        mycursor.execute("SELECT * FROM complainttable WHERE Slno = %s ORDER BY Slno", (CmbBox,))
        record2 = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM complainttable ORDER BY Slno")
        record2 = mycursor.fetchall()
        
    mycursor.close()
    conn.close()
    return render(request, 'ComplaintReport.html', {'record1': record1, 'record2': record2})

# --- CONTACT US REPORT ---
def ContactUsReport(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM contactus ORDER BY Slno")
    record1 = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return render(request, 'ContactUsReport.html', {'record1': record1, 'record2': None})

def ConReportSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM contactus ORDER BY Slno")
    record1 = mycursor.fetchall()
    
    CmbBox = request.POST.get('CmbBox')
    if CmbBox and CmbBox != "All" and CmbBox != "-Select-":
        mycursor.execute("SELECT * FROM contactus WHERE Slno = %s ORDER BY Slno", (CmbBox,))
        record2 = mycursor.fetchall()
    else:
        mycursor.execute("SELECT * FROM contactus ORDER BY Slno")
        record2 = mycursor.fetchall()
        
    mycursor.close()
    conn.close()
    return render(request, 'ContactUsReport.html', {'record1': record1, 'record2': record2})
