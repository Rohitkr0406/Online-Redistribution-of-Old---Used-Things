import pymysql
from django.shortcuts import render
from auth_system.decorators import admin_required
from auth_system.db_helper import get_db_connection

# --- COLLECTION VIEWS ---
@admin_required
def Collection(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    record1 = []
    record = None
    val = []
    try:
        # Fetch list of product IDs from unusedthing to populate dropdown
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        # Fetch list of Serial numbers for search dropdown
        mycursor.execute("SELECT Slno, Proid, DonBy FROM collectiontable")
        record1 = mycursor.fetchall()
    except Exception as e:
        msg = f"Error: {str(e)}"
    finally:
        mycursor.close()
        conn.close()
    return render(request, 'Collection.html', {'val': val, 'record1': record1, 'msg': msg, 'record': record})

@admin_required
def CollectionSave(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    
    Slno1 = request.POST.get('Slno')
    Proid1 = request.POST.get('Proid')
    CollQty1 = request.POST.get('CollQty')
    RecDate1 = request.POST.get('RecDate')
    Status1 = request.POST.get('Status')
    DonBy1 = request.POST.get('DonBy')
    DonorAdd1 = request.POST.get('DonorAdd')
    RecBy1 = request.POST.get('RecBy')
    Remarks1 = request.POST.get('Remarks')
    
    ps = (Slno1, Proid1, CollQty1, RecDate1, Status1, DonBy1, DonorAdd1, RecBy1, Remarks1)
    try:
        mycursor.execute(
            """INSERT INTO collectiontable(Slno, Proid, CollQty, RecDate, Status, DonBy, DonorAdd, RecBy, Remarks) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", ps)
        conn.commit()
        msg = "Data Saved Successfully..!!"
    except Exception as e:
        msg = f"Wrong Data Entry: {str(e)}"
    finally:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, DonBy FROM collectiontable")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    return render(request, 'Collection.html', {'msg': msg, 'val': val, 'record1': record1, 'record': None})

@admin_required
def CollectionDelete(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    Proid1 = request.POST.get('Proid')
    try:
        mycursor.execute("DELETE FROM collectiontable WHERE Proid = %s", (Proid1,))
        conn.commit()
        msg = "One Record Deleted Successfully..!!"
    except Exception as e:
        msg = f"Record Not Found: {str(e)}"
    finally:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, DonBy FROM collectiontable")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    return render(request, 'Collection.html', {'msg': msg, 'val': val, 'record1': record1, 'record': None})

@admin_required
def CollectionSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    CmbBox1 = request.POST.get('CmbBox')
    record = None
    msg = ""
    
    if CmbBox1 in ["Select", "-Select-", "", None]:
        msg = "Data Not found.....!!"
    else:
        try:
            mycursor.execute("SELECT * FROM collectiontable WHERE Slno=%s", (CmbBox1,))
            val_records = mycursor.fetchall()
            if val_records:
                record = val_records[0]
                msg = "One Record Search Successfully.....!!"
            else:
                msg = "Data Not found.....!!"
        except Exception as e:
            msg = f"Data Not found: {str(e)}"
            
    try:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, DonBy FROM collectiontable")
        record1 = mycursor.fetchall()
    except Exception as e:
        record1 = []
        val = []
    finally:
        mycursor.close()
        conn.close()
    return render(request, 'Collection.html', {'msg': msg, 'val': val, 'record1': record1, 'record': record})

@admin_required
def CollectionUpdate(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    
    Slno1 = request.POST.get('Slno')
    Proid1 = request.POST.get('Proid')
    CollQty1 = request.POST.get('CollQty')
    RecDate1 = request.POST.get('RecDate')
    Status1 = request.POST.get('Status')
    DonBy1 = request.POST.get('DonBy')
    DonorAdd1 = request.POST.get('DonorAdd')
    RecBy1 = request.POST.get('RecBy')
    Remarks1 = request.POST.get('Remarks')
    
    try:
        mycursor.execute(
            """UPDATE collectiontable SET Slno=%s, CollQty=%s, RecDate=%s, Status=%s, DonBy=%s, DonorAdd=%s, RecBy=%s, Remarks=%s 
            WHERE Proid=%s""", (Slno1, CollQty1, RecDate1, Status1, DonBy1, DonorAdd1, RecBy1, Remarks1, Proid1))
        conn.commit()
        msg = "Record Updated Successfully..!!"
    except Exception as e:
        msg = f"Update Failed: {str(e)}"
    finally:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, DonBy FROM collectiontable")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    return render(request, 'Collection.html', {'msg': msg, 'val': val, 'record1': record1, 'record': None})


# --- STOCK VIEWS ---
@admin_required
def Stock(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    record1 = []
    val = []
    try:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, Pname FROM stockdetails")
        record1 = mycursor.fetchall()
    except Exception as e:
        msg = f"Error: {str(e)}"
    finally:
        mycursor.close()
        conn.close()
    return render(request, 'Stock.html', {'val': val, 'record1': record1, 'msg': msg, 'record': None})

@admin_required
def StockSave(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    
    Slno1 = request.POST.get('Slno')
    Proid1 = request.POST.get('Proid')
    Pname1 = request.POST.get('Pname')
    Cate1 = request.POST.get('cate')
    SubCate1 = request.POST.get('SubCate')
    ProSlno1 = request.POST.get('ProSlno')
    BatchNo1 = request.POST.get('BatchNo')
    DisAmt1 = request.POST.get('DisAmt')
    StockAmt1 = request.POST.get('StockAmt')
    Remarks1 = request.POST.get('Remarks')
    
    ps = (Slno1, Proid1, Pname1, Cate1, SubCate1, ProSlno1, BatchNo1, DisAmt1, StockAmt1, Remarks1)
    try:
        mycursor.execute(
            """INSERT INTO stockdetails(Slno, Proid, Pname, Cate, SubCate, ProSlno, BatchNo, DisAmt, StockAmt, Remarks) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", ps)
        conn.commit()
        msg = "Data Saved Successfully..!!"
    except Exception as e:
        msg = f"Wrong Data Entry: {str(e)}"
    finally:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, Pname FROM stockdetails")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    return render(request, 'Stock.html', {'msg': msg, 'val': val, 'record1': record1, 'record': None})

@admin_required
def StockDelete(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    Proid1 = request.POST.get('Proid')
    try:
        mycursor.execute("DELETE FROM stockdetails WHERE Proid = %s", (Proid1,))
        conn.commit()
        msg = "One Record Deleted Successfully..!!"
    except Exception as e:
        msg = f"Record Not Found: {str(e)}"
    finally:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, Pname FROM stockdetails")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    return render(request, 'Stock.html', {'msg': msg, 'val': val, 'record1': record1, 'record': None})

@admin_required
def StockSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    CmbBox1 = request.POST.get('CmbBox')
    record = None
    msg = ""
    
    if CmbBox1 in ["Select", "-Select-", "", None]:
        msg = "Data Not found.....!!"
    else:
        try:
            mycursor.execute("SELECT * FROM stockdetails WHERE Slno=%s", (CmbBox1,))
            val_records = mycursor.fetchall()
            if val_records:
                record = val_records[0]
                msg = "One Record Search Successfully.....!!"
            else:
                msg = "Data Not found.....!!"
        except Exception as e:
            msg = f"Data Not found: {str(e)}"
            
    try:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, Pname FROM stockdetails")
        record1 = mycursor.fetchall()
    except Exception as e:
        record1 = []
        val = []
    finally:
        mycursor.close()
        conn.close()
    return render(request, 'Stock.html', {'msg': msg, 'val': val, 'record1': record1, 'record': record})

@admin_required
def StockUpdate(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    
    Slno1 = request.POST.get('Slno')
    Proid1 = request.POST.get('Proid')
    Pname1 = request.POST.get('Pname')
    Cate1 = request.POST.get('cate')
    SubCate1 = request.POST.get('SubCate')
    ProSlno1 = request.POST.get('ProSlno')
    BatchNo1 = request.POST.get('BatchNo')
    DisAmt1 = request.POST.get('DisAmt')
    StockAmt1 = request.POST.get('StockAmt')
    Remarks1 = request.POST.get('Remarks')
    
    try:
        mycursor.execute(
            """UPDATE stockdetails SET Slno=%s, Pname=%s, Cate=%s, SubCate=%s, ProSlno=%s, BatchNo=%s, DisAmt=%s, StockAmt=%s, Remarks=%s 
            WHERE Proid=%s""", (Slno1, Pname1, Cate1, SubCate1, ProSlno1, BatchNo1, DisAmt1, StockAmt1, Remarks1, Proid1))
        conn.commit()
        msg = "Record Updated Successfully..!!"
    except Exception as e:
        msg = f"Update Failed: {str(e)}"
    finally:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, Pname FROM stockdetails")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    return render(request, 'Stock.html', {'msg': msg, 'val': val, 'record1': record1, 'record': None})


# --- DISTRIBUTION VIEWS ---
@admin_required
def Distribution(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    record1 = []
    val = []
    try:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, RecName FROM distributetable")
        record1 = mycursor.fetchall()
    except Exception as e:
        msg = f"Error: {str(e)}"
    finally:
        mycursor.close()
        conn.close()
    return render(request, 'Distribution.html', {'val': val, 'record1': record1, 'msg': msg, 'record': None})

@admin_required
def DistributionSave(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    
    Slno1 = request.POST.get('Slno')
    Proid1 = request.POST.get('Proid')
    DisQty1 = request.POST.get('DisQty')
    DisDate1 = request.POST.get('DisDate')
    DisBy1 = request.POST.get('DisBy')
    RecName1 = request.POST.get('RecName')
    RecAdd1 = request.POST.get('RecAdd')
    RecMob1 = request.POST.get('RecMob')
    RecBy1 = request.POST.get('RecBy')
    Remarks1 = request.POST.get('Remarks')
    
    ps = (Slno1, Proid1, DisQty1, DisDate1, DisBy1, RecName1, RecAdd1, RecMob1, RecBy1, Remarks1)
    try:
        mycursor.execute(
            """INSERT INTO distributetable(Slno, Proid, DisQty, DisDate, DisBy, RecName, RecAdd, RecMob, RecBy, Remarks) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", ps)
        conn.commit()
        msg = "Data Saved Successfully..!!"
    except Exception as e:
        msg = f"Wrong Data Entry: {str(e)}"
    finally:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, RecName FROM distributetable")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    return render(request, 'Distribution.html', {'msg': msg, 'val': val, 'record1': record1, 'record': None})

@admin_required
def DistributionDelete(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    Proid1 = request.POST.get('Proid')
    try:
        mycursor.execute("DELETE FROM distributetable WHERE Proid = %s", (Proid1,))
        conn.commit()
        msg = "One Record Deleted Successfully..!!"
    except Exception as e:
        msg = f"Record Not Found: {str(e)}"
    finally:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, RecName FROM distributetable")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    return render(request, 'Distribution.html', {'msg': msg, 'val': val, 'record1': record1, 'record': None})

@admin_required
def DistributionSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    CmbBox1 = request.POST.get('CmbBox')
    record = None
    msg = ""
    
    if CmbBox1 in ["Select", "-Select-", "", None]:
        msg = "Data Not found.....!!"
    else:
        try:
            mycursor.execute("SELECT * FROM distributetable WHERE Slno=%s", (CmbBox1,))
            val_records = mycursor.fetchall()
            if val_records:
                record = val_records[0]
                msg = "One Record Search Successfully.....!!"
            else:
                msg = "Data Not found.....!!"
        except Exception as e:
            msg = f"Data Not found: {str(e)}"
            
    try:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, RecName FROM distributetable")
        record1 = mycursor.fetchall()
    except Exception as e:
        record1 = []
        val = []
    finally:
        mycursor.close()
        conn.close()
    return render(request, 'Distribution.html', {'msg': msg, 'val': val, 'record1': record1, 'record': record})

@admin_required
def DistributionUpdate(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    
    Slno1 = request.POST.get('Slno')
    Proid1 = request.POST.get('Proid')
    DisQty1 = request.POST.get('DisQty')
    DisDate1 = request.POST.get('DisDate')
    DisBy1 = request.POST.get('DisBy')
    RecName1 = request.POST.get('RecName')
    RecAdd1 = request.POST.get('RecAdd')
    RecMob1 = request.POST.get('RecMob')
    RecBy1 = request.POST.get('RecBy')
    Remarks1 = request.POST.get('Remarks')
    
    try:
        mycursor.execute(
            """UPDATE distributetable SET Slno=%s, DisQty=%s, DisDate=%s, DisBy=%s, RecName=%s, RecAdd=%s, RecMob=%s, RecBy=%s, Remarks=%s 
            WHERE Proid=%s""", (Slno1, DisQty1, DisDate1, DisBy1, RecName1, RecAdd1, RecMob1, RecBy1, Remarks1, Proid1))
        conn.commit()
        msg = "Record Updated Successfully..!!"
    except Exception as e:
        msg = f"Update Failed: {str(e)}"
    finally:
        mycursor.execute("SELECT Proid FROM unusedthing")
        val = mycursor.fetchall()
        mycursor.execute("SELECT Slno, Proid, RecName FROM distributetable")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    return render(request, 'Distribution.html', {'msg': msg, 'val': val, 'record1': record1, 'record': None})
