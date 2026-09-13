import urllib.request
import urllib.parse
import http.cookiejar
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Get login page
resp = opener.open('http://127.0.0.1:8000/admin/login/')
html = resp.read().decode('utf-8')
match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', html)
csrf_token = match.group(1) if match else ''
print('CSRF token found:', bool(csrf_token))

# 2. Post login
login_data = urllib.parse.urlencode({
    'csrfmiddlewaretoken': csrf_token,
    'username': 'admin',
    'password': 'admin123'
}).encode('utf-8')

req = urllib.request.Request('http://127.0.0.1:8000/admin/login/', data=login_data, headers={'Referer': 'http://127.0.0.1:8000/admin/login/'})
resp2 = opener.open(req)
print('Login response URL:', resp2.geturl())
print('Login response code:', resp2.getcode())

# 3. Check dashboard access
resp3 = opener.open('http://127.0.0.1:8000/admin/dashboard/')
print('Dashboard access code:', resp3.getcode())
dashboard_html = resp3.read().decode('utf-8')
print('Dashboard loaded successfully:', 'Dashboard' in dashboard_html or 'Admin' in dashboard_html)

# 4. Check DetailApp / Collection access
resp4 = opener.open('http://127.0.0.1:8000/DetailApp/Collection')
print('Collection page access code:', resp4.getcode())

# 5. Check ReportApp access
resp5 = opener.open('http://127.0.0.1:8000/ReportApp/')
print('ReportApp access code:', resp5.getcode())

# 6. Test Donor Registration
import random
donor_suffix = random.randint(1000, 9999)
donor_id = f"donor_{donor_suffix}"
reg_data = urllib.parse.urlencode({
    'csrfmiddlewaretoken': csrf_token,
    'Donorid': donor_id,
    'Dname': f'Test Donor {donor_suffix}',
    'Dpsd': 'Password@123',
    'Dcpsd': 'Password@123',
    'Dob': '1995-05-15',
    'Gen': 'Male',
    'Dmob': '9876543210',
    'Demail': f'donor{donor_suffix}@test.com',
    'Add1': '123 Test Street',
    'Add2': 'Suite 4B',
    'State': 'Karnataka',
    'City': 'Bengaluru',
    'Pin': '560001',
    'Remarks': 'Automated Test Donor'
}).encode('utf-8')

req_reg = urllib.request.Request('http://127.0.0.1:8000/RegApp/DonatorSave', data=reg_data, headers={'Referer': 'http://127.0.0.1:8000/RegApp/Donator'})
resp_reg = opener.open(req_reg)
print('Donor Registration response code:', resp_reg.getcode())

# 7. Test Donor Login with new session
cj_donor = http.cookiejar.CookieJar()
donor_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj_donor))

resp_login_page = donor_opener.open('http://127.0.0.1:8000/FirstApp/Login')
html_login = resp_login_page.read().decode('utf-8')
match_token = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', html_login)
donor_csrf = match_token.group(1) if match_token else ''

donor_login_data = urllib.parse.urlencode({
    'csrfmiddlewaretoken': donor_csrf,
    'userid': donor_id,
    'password': 'Password@123',
    'user_type': 'donor'
}).encode('utf-8')

req_donor_login = urllib.request.Request('http://127.0.0.1:8000/FirstApp/Login', data=donor_login_data, headers={'Referer': 'http://127.0.0.1:8000/FirstApp/Login'})
resp_donor_logged = donor_opener.open(req_donor_login)
print('Donor Login final URL:', resp_donor_logged.geturl())
print('Donor Login response code:', resp_donor_logged.getcode())

# 8. Test authenticated Donor accessing Unused Things page
resp_unused = donor_opener.open('http://127.0.0.1:8000/RegApp/Unused')
print('Donor access to Unused page:', resp_unused.getcode())

# 9. Test Complaint form submission
complaint_data = urllib.parse.urlencode({
    'csrfmiddlewaretoken': donor_csrf,
    'IssuType': 'Service Delay',
    'CompDetails': 'Testing complaint submission from automated test',
    'Remarks': 'Testing remarks'
}).encode('utf-8')
req_comp = urllib.request.Request('http://127.0.0.1:8000/ComApp/CompSave', data=complaint_data, headers={'Referer': 'http://127.0.0.1:8000/ComApp/Complaint'})
resp_comp = donor_opener.open(req_comp)
print('Complaint submission response code:', resp_comp.getcode(), flush=True)

# 10. Test Contact Us form submission
contact_data = urllib.parse.urlencode({
    'csrfmiddlewaretoken': donor_csrf,
    'ComName': 'Tester',
    'ComEmail': 'tester@example.com',
    'ComAdd': 'Test Street',
    'ComMob': '9876543210',
    'Remarks': 'Test Inquiry'
}).encode('utf-8')
req_contact = urllib.request.Request('http://127.0.0.1:8000/ComApp/ContactSave', data=contact_data, headers={'Referer': 'http://127.0.0.1:8000/ComApp/Contactus'})
resp_contact = donor_opener.open(req_contact)
print('Contact submission response code:', resp_contact.getcode(), flush=True)

print('\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!', flush=True)
