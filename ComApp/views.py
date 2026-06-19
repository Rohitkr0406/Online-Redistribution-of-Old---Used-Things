import pymysql
from django.shortcuts import render

def get_db_connection():
    return pymysql.connect(host='localhost', user='root', passwd='destroyer3607', db='stud')

def Complaint(request):
    return render(request, 'Complaint.html', {'msg': ''})

def CompSave(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    
    Slno1 = request.POST.get('Slno')
    Did1 = request.POST.get('Did')
    CompDate1 = request.POST.get('CompDate')
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
    return render(request, 'Complaint.html', {'msg': msg})

def Contactus(request):
    return render(request, 'ContactUs.html', {'msg': ''})

def ContactSave(request):
    conn = get_db_connection()
    mycursor = conn.cursor()
    msg = ""
    
    Slno1 = request.POST.get('Slno')
    Admid1 = request.POST.get('Admid')
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
    return render(request, 'ContactUs.html', {'msg': msg})
