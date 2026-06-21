import pymysql
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from auth_system.decorators import admin_required, donor_required
from auth_system.db_helper import get_db_connection

def Donator(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    record = None
    record1 = []
    
    # Privacy rule: Only fetch other donors if user is logged in as an administrator
    if request.session.get('admin_id'):
        try:
            mycursor.execute("""SELECT Slno, Donorid, Dname FROM donorreg""")
            record1 = mycursor.fetchall()
        except Exception as e:
            msg = "Wrong Data Entry..!!"
            print(msg)
    
    mycursor.close()
    conn.close()
    
    return render(request, 'Donator.html', {'record1': record1, 'msg': msg, 'record': record})


def DonatorSave(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    
    Slno1 = request.POST.get('Slno')
    Dname1 = request.POST.get('Dname')
    Donorid1 = request.POST.get('Donorid')
    Dpsd1 = request.POST.get('Dpsd')
    Dcpsd1 = request.POST.get('Dcpsd')
    Dob1 = request.POST.get('Dob')
    Gen1 = request.POST.get('Gen')
    Dmob1 = request.POST.get('Dmob')
    Demail1 = request.POST.get('Demail')
    Add11 = request.POST.get('Add1')
    Add21 = request.POST.get('Add2')
    State1 = request.POST.get('State')
    City1 = request.POST.get('City')
    Pin1 = request.POST.get('Pin')
    Remarks1 = request.POST.get('Remarks')
    
    # Hash password securely before database insertion!
    hashed_pw = make_password(Dpsd1)
    
    ps = (Slno1, Donorid1, Dname1, hashed_pw, hashed_pw, Dob1, Gen1, Dmob1, Demail1, Add11, Add21, State1, City1, Pin1, Remarks1)
    
    try:
        mycursor.execute(
            """INSERT INTO donorreg(Slno, Donorid, Dname, Dpsd, Dcpsd, Dob, Gen, Dmob, Demail, Add1, Add2, State, City, Pin, Remarks) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", ps)
        conn.commit()
        msg = "Data Saved Successfully..!!"
        print(msg)
    except Exception as e:
        msg = f"Wrong Data Entry: {str(e)}"
        print(msg)
    
    record1 = []
    # If admin is registering/saving:
    is_admin = request.session.get('admin_id') is not None
    if is_admin:
        mycursor.execute("""SELECT Slno, Donorid, Dname FROM donorreg""")
        record1 = mycursor.fetchall()
        
    mycursor.close()
    conn.close()
    
    # Redirect public registration to login with success message
    if "Successfully" in msg and not is_admin:
        messages.success(request, "Registration successful! Please log in with your credentials.")
        return redirect('/FirstApp/Login')
        
    return render(request, 'Donator.html', {'msg': msg, 'record1': record1, 'record': None})


@admin_required
def DonatorDelete(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    Donorid1 = request.POST.get('Donorid')
    
    try:
        mycursor.execute("""DELETE FROM donorreg WHERE Donorid = %s""", (Donorid1,))
        conn.commit()
        msg = "One Record Deleted Successfully..!!"
        print(msg)
    except Exception as e:
        msg = f"Record Not Found: {str(e)}"
        print(msg)
    finally:
        mycursor.execute("""SELECT Slno, Donorid, Dname FROM donorreg""")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    
    return render(request, 'Donator.html', {'msg': msg, 'record1': record1, 'record': None})


@admin_required
def DonatorSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    CmbBox1 = request.POST.get('CmbBox')
    record = None
    
    if CmbBox1 == "Select" or CmbBox1 == "-Select-" or CmbBox1 == "":
        record = None
        msg = "Data Not found.....!!"
        try:
            mycursor.execute("""SELECT Slno, Donorid, Dname FROM donorreg""")
            record1 = mycursor.fetchall()
        except Exception as e:
            msg = "Wrong Data Entry..!!"
            record1 = []
        finally:
            mycursor.close()
            conn.close()
    else:
        try:
            mycursor.execute("""SELECT * FROM donorreg WHERE Slno=%s""", (CmbBox1,))
            val = mycursor.fetchall()
            if val:
                row = val[0]
                record = row[:11]
                msg = "One Record Search Successfully.....!!"
            else:
                record = None
                msg = "Data Not found.....!!"
        except Exception as e:
            msg = f"Data Not found: {str(e)}"
            record = None
        finally:
            mycursor.execute("""SELECT Slno, Donorid, Dname FROM donorreg""")
            record1 = mycursor.fetchall()
            mycursor.close()
            conn.close()
    
    return render(request, 'Donator.html', {'msg': msg, 'record1': record1, 'record': record})


@admin_required
def DonatorUpdate(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    
    Donorid1 = request.POST.get('Donorid')
    Dname1 = request.POST.get('Dname')
    Dpsd1 = request.POST.get('Dpsd')
    Dcpsd1 = request.POST.get('Dcpsd')
    Dob1 = request.POST.get('Dob')
    Gen1 = request.POST.get('Gen')
    Dmob1 = request.POST.get('Dmob')
    Demail1 = request.POST.get('Demail')
    Add11 = request.POST.get('Add1')
    Add21 = request.POST.get('Add2')
    State1 = request.POST.get('State')
    City1 = request.POST.get('City')
    Pin1 = request.POST.get('Pin')
    Remarks1 = request.POST.get('Remarks')
    
    # Hash password if updating it and it's not already hashed
    if Dpsd1 and not Dpsd1.startswith('pbkdf2_sha256$'):
        hashed_pw = make_password(Dpsd1)
    else:
        hashed_pw = Dpsd1
        
    try:
        mycursor.execute(
            """UPDATE donorreg SET Dname=%s, Dpsd=%s, Dcpsd=%s, Dob=%s, Gen=%s, Dmob=%s, Demail=%s, Add1=%s, Add2=%s, State=%s, City=%s, Pin=%s, Remarks=%s WHERE Donorid=%s""",
            (Dname1, hashed_pw, hashed_pw, Dob1, Gen1, Dmob1, Demail1, Add11, Add21, State1, City1, Pin1, Remarks1, Donorid1))
        conn.commit()
        msg = "Record Updated Successfully..!!"
        print(msg)
    except Exception as e:
        msg = f"Update Failed: {str(e)}"
        print(msg)
    finally:
        mycursor.execute("""SELECT Slno, Donorid, Dname FROM donorreg""")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    
    return render(request, 'Donator.html', {'msg': msg, 'record1': record1, 'record': None})


@donor_required
def Unused(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    record = None
    
    try:
        mycursor.execute("""SELECT Slno, Proid, ProName FROM unusedthing""")
        record1 = mycursor.fetchall()
    except Exception as e:
        msg = "Wrong Data Entry..!!"
        record1 = []
        print(msg)
    finally:
        mycursor.close()
        conn.close()
    
    return render(request, 'UnUsed.html', {'msg': msg, 'record1': record1, 'record': record})


@donor_required
def UnusedSave(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    
    Slno1 = request.POST.get('Slno')
    Proid1 = request.POST.get('Proid')
    ProName1 = request.POST.get('ProName')
    ProCate1 = request.POST.get('ProCate')
    ProSubCate1 = request.POST.get('ProSubCate')
    ProSerial1 = request.POST.get('ProSerial')
    ProBatchno1 = request.POST.get('ProBatchno')
    PurchDate1 = request.POST.get('PurchDate')
    Status1 = request.POST.get('Status')
    Remarks1 = request.POST.get('Remarks')
    
    ps = (Slno1, Proid1, ProName1, ProCate1, ProSubCate1, ProSerial1, ProBatchno1, PurchDate1, Status1, Remarks1)
    
    try:
        mycursor.execute(
            """INSERT INTO unusedthing(Slno, Proid, ProName, ProCate, ProSubCate, ProSerial, ProBatchno, PurchDate, Status, Remarks) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", ps)
        conn.commit()
        msg = "Data Saved Successfully..!!"
        print(msg)
    except Exception as e:
        msg = f"Wrong Data Entry: {str(e)}"
        print(msg)
    finally:
        mycursor.execute("""SELECT Slno, Proid, ProName FROM unusedthing""")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    
    return render(request, 'UnUsed.html', {'msg': msg, 'record1': record1, 'record': None})


@donor_required
def UnusedDelete(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    Proid1 = request.POST.get('Proid')
    
    try:
        mycursor.execute("""DELETE FROM unusedthing WHERE Proid = %s""", (Proid1,))
        conn.commit()
        msg = "One Record Deleted Successfully..!!"
        print(msg)
    except Exception as e:
        msg = f"Record Not Found: {str(e)}"
        print(msg)
    finally:
        mycursor.execute("""SELECT Slno, Proid, ProName FROM unusedthing""")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    
    return render(request, 'UnUsed.html', {'msg': msg, 'record1': record1, 'record': None})


@donor_required
def UnusedSearch(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    CmbBox1 = request.POST.get('CmbBox')
    record = None
    
    if CmbBox1 == "Select" or CmbBox1 == "-Select-" or CmbBox1 == "":
        record = None
        msg = "Data Not found.....!!"
        try:
            mycursor.execute("""SELECT Slno, Proid, ProName FROM unusedthing""")
            record1 = mycursor.fetchall()
        except Exception as e:
            msg = "Wrong Data Entry..!!"
            record1 = []
        finally:
            mycursor.close()
            conn.close()
    else:
        try:
            mycursor.execute("""SELECT * FROM unusedthing WHERE Slno=%s""", (CmbBox1,))
            val = mycursor.fetchall()
            if val:
                row = val[0]
                record = row[:10]
                msg = "One Record Search Successfully.....!!"
            else:
                record = None
                msg = "Data Not found.....!!"
        except Exception as e:
            msg = f"Data Not found: {str(e)}"
            record = None
        finally:
            mycursor.execute("""SELECT Slno, Proid, ProName FROM unusedthing""")
            record1 = mycursor.fetchall()
            mycursor.close()
            conn.close()
    
    return render(request, 'UnUsed.html', {'msg': msg, 'record1': record1, 'record': record})


@donor_required
def UnusedUpdate(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    
    Proid1 = request.POST.get('Proid')
    ProName1 = request.POST.get('ProName')
    ProCate1 = request.POST.get('ProCate')
    ProSubCate1 = request.POST.get('ProSubCate')
    ProSerial1 = request.POST.get('ProSerial')
    ProBatchno1 = request.POST.get('ProBatchno')
    PurchDate1 = request.POST.get('PurchDate')
    Status1 = request.POST.get('Status')
    Remarks1 = request.POST.get('Remarks')
    
    try:
        mycursor.execute(
            """UPDATE unusedthing SET ProName=%s, ProCate=%s, ProSubCate=%s, ProSerial=%s, ProBatchno=%s, PurchDate=%s, Status=%s, Remarks=%s WHERE Proid=%s""",
            (ProName1, ProCate1, ProSubCate1, ProSerial1, ProBatchno1, PurchDate1, Status1, Remarks1, Proid1))
        conn.commit()
        msg = "Record Updated Successfully..!!"
        print(msg)
    except Exception as e:
        msg = f"Update Failed: {str(e)}"
        print(msg)
    finally:
        mycursor.execute("""SELECT Slno, Proid, ProName FROM unusedthing""")
        record1 = mycursor.fetchall()
        mycursor.close()
        conn.close()
    
    return render(request, 'UnUsed.html', {'msg': msg, 'record1': record1, 'record': None})
