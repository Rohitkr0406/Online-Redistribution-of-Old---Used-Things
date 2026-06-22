import pymysql
import datetime
from django.shortcuts import render
from auth_system.db_helper import get_db_connection
from auth_system.decorators import donor_required

@donor_required
def Complaint(request):
    donor_id = request.session.get('donor_id', '')
    today = datetime.date.today().strftime('%Y-%m-%d')
    return render(request, 'Complaint.html', {
        'msg': '', 
        'donor_id': donor_id, 
        'today_date': today
    })

@donor_required
def CompSave(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    
    # Auto-generate Slno
    mycursor.execute("SELECT COALESCE(MAX(Slno), 0) FROM complainttable")
    row = mycursor.fetchone()
    max_slno = row[0] if row and row[0] is not None else 0
    Slno1 = max_slno + 1
    
    Did1 = request.session.get('donor_id')
    CompDate1 = datetime.date.today()
    IssuType1 = request.POST.get('IssuType')
    CompDetails1 = request.POST.get('CompDetails')
    Remarks1 = request.POST.get('Remarks')
    
    ps = (Slno1, Did1, CompDate1, IssuType1, CompDetails1, Remarks1)
    try:
        mycursor.execute(
            """INSERT INTO complainttable(Slno, Did, CompDate, IssuType, CompDetails, Remarks) 
            VALUES (%s,%s,%s,%s,%s,%s)""", ps)
        conn.commit()
        msg = "Data Saved Successfully..!!"
    except Exception as e:
        msg = f"Wrong Data Entry: {str(e)}"
    finally:
        mycursor.close()
        conn.close()
        
    today = datetime.date.today().strftime('%Y-%m-%d')
    return render(request, 'Complaint.html', {
        'msg': msg, 
        'donor_id': Did1, 
        'today_date': today
    })

def Contactus(request):
    donor_name = request.session.get('donor_name', '')
    donor_email = ""
    donor_mob = ""
    donor_add = ""
    donor_id = request.session.get('donor_id')
    
    if donor_id:
        conn = get_db_connection()
        mycursor = conn.cursor()
        try:
            mycursor.execute("SELECT Demail, Dmob, Add1, Add2 FROM donorreg WHERE Donorid = %s", (donor_id,))
            row = mycursor.fetchone()
            if row:
                donor_email = row[0]
                donor_mob = row[1]
                donor_add = f"{row[2]}, {row[3]}" if row[3] else row[2]
        except Exception as e:
            print(f"Error fetching donor details for prefill: {e}")
        finally:
            mycursor.close()
            conn.close()
            
    return render(request, 'ContactUs.html', {
        'msg': '',
        'donor_name': donor_name,
        'donor_email': donor_email,
        'donor_mob': donor_mob,
        'donor_add': donor_add
    })

def ContactSave(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    
    # Auto-generate Slno
    mycursor.execute("SELECT COALESCE(MAX(Slno), 0) FROM contactus")
    row = mycursor.fetchone()
    max_slno = row[0] if row and row[0] is not None else 0
    Slno1 = max_slno + 1
    
    # Default to the primary admin account
    Admid1 = 'admin'
    
    ComName1 = request.POST.get('ComName')
    ComEmail1 = request.POST.get('ComEmail')
    ComAdd1 = request.POST.get('ComAdd')
    ComMob1 = request.POST.get('ComMob')
    Remarks1 = request.POST.get('Remarks')
    
    ps = (Slno1, Admid1, ComName1, ComEmail1, ComAdd1, ComMob1, Remarks1)
    try:
        mycursor.execute(
            """INSERT INTO contactus(Slno, Admid, ComName, ComEmail, ComAdd, ComMob, Remarks) 
            VALUES (%s,%s,%s,%s,%s,%s,%s)""", ps)
        conn.commit()
        msg = "Data Saved Successfully..!!"
    except Exception as e:
        msg = f"Wrong Data Entry: {str(e)}"
    finally:
        mycursor.close()
        conn.close()
        
    return render(request, 'ContactUs.html', {
        'msg': msg,
        'donor_name': ComName1,
        'donor_email': ComEmail1,
        'donor_mob': ComMob1,
        'donor_add': ComAdd1
    })
