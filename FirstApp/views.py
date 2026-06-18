from django.shortcuts import render
import pymysql


def Home(request):
    return render(request, 'Home.html')


def ConnecivityPage(request):
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd='destroyer3607', db='stud')
        mycursor = conn.cursor()
        msg = "Database Connected Successfully..."
        mycursor.close()
        conn.close()
    except Exception as e:
        msg = f"Database Connection Failed: {str(e)}"
    
    return render(request, 'Connectivity.html', {'msg': msg})
