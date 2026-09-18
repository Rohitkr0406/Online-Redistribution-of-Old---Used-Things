from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from auth_system.decorators import admin_required, recipient_required
from auth_system.session_manager import start_recipient_session, logout_recipient
from django.contrib.admin.views.decorators import staff_member_required
from RegApp.models import DonorReg, UnusedThing
from ComApp.models import ComplaintTable, ContactUs
from .models import CollectionTable, StockDetails, DistributeTable, Recipient, DonationRequest


# ==============================================================================
# 1. RECIPIENT AUTHENTICATION VIEWS
# ==============================================================================

def RecipientRegister(request):
    """
    Registers a new recipient (needy person).
    """
    msg = ""
    # Suggest next auto-incremented Recipient ID
    count = Recipient.objects.count() + 1
    suggested_id = f"REC{100 + count}"
    while Recipient.objects.filter(recipient_id=suggested_id).exists():
        count += 1
        suggested_id = f"REC{100 + count}"

    if request.method == 'POST':
        recipient_id = (request.POST.get('Recipientid') or suggested_id).strip()
        name = request.POST.get('Name', '').strip()
        email = request.POST.get('Email', '').strip()
        mobile = request.POST.get('Mobile', '').strip()
        address = request.POST.get('Address', '').strip()
        city = request.POST.get('City', '').strip()
        state = request.POST.get('State', '').strip()
        pin = request.POST.get('Pin', '').strip()
        password = request.POST.get('Password', '')
        cpassword = request.POST.get('CPassword', '')
        remarks = request.POST.get('Remarks', '').strip()

        # Validation checks
        if not name or not email or not mobile or not address or not city or not state:
            messages.error(request, "Please fill in all required fields.")
        elif password != cpassword:
            messages.error(request, "Password and Confirm Password do not match.")
        elif len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
        elif Recipient.objects.filter(recipient_id__iexact=recipient_id).exists():
            messages.error(request, f"Recipient ID '{recipient_id}' is already taken.")
        elif Recipient.objects.filter(email__iexact=email).exists():
            messages.error(request, f"Email '{email}' is already registered.")
        else:
            try:
                # Auto calculate serial number
                with connection.cursor() as cur:
                    cur.execute("SELECT COALESCE(MAX(Slno), 0) FROM recipient")
                    row = cur.fetchone()
                    next_slno = (row[0] if row and row[0] is not None else 0) + 1

                hashed_password = make_password(password)
                recipient = Recipient(
                    slno=next_slno,
                    recipient_id=recipient_id,
                    name=name,
                    email=email,
                    mobile=mobile,
                    address=address,
                    city=city,
                    state=state,
                    pin=pin,
                    password=hashed_password,
                    remarks=remarks,
                    userrole='recipient'
                )
                recipient.save()

                # Automatically log in new recipient
                start_recipient_session(request, recipient.recipient_id, recipient.name)
                messages.success(request, f"Registration successful! Welcome to SUTD, {recipient.name}.")
                return redirect('AvailableItems')
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")

    return render(request, 'RecipientRegister.html', {'suggested_id': suggested_id})


def RecipientLogin(request):
    """
    Dedicated login view for recipients.
    """
    if request.method == 'POST':
        login_id = (request.POST.get('userid') or '').strip()
        password = request.POST.get('password') or ''

        recipient = Recipient.objects.filter(
            Q(recipient_id__iexact=login_id) | Q(email__iexact=login_id)
        ).first()

        if recipient:
            if check_password(password, recipient.password):
                start_recipient_session(request, recipient.recipient_id, recipient.name)
                messages.success(request, f"Welcome back, {recipient.name}!")
                next_url = request.GET.get('next') or '/DetailApp/AvailableItems'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid password for Recipient account.")
        else:
            messages.error(request, "Recipient ID or Email not found. Please register.")

    return render(request, 'RecipientLogin.html')


def RecipientLogout(request):
    """
    Logs out the recipient and redirects to the home page.
    """
    logout_recipient(request)
    messages.info(request, "Recipient logged out successfully.")
    return redirect('/')


# ==============================================================================
# 2. AVAILABLE STOCK & CATALOG VIEWS
# ==============================================================================

def AvailableItems(request):
    """
    Displays all donated items currently eligible/available for redistribution.
    """
    category = request.GET.get('category', '').strip()
    query = request.GET.get('q', '').strip()

    items = UnusedThing.objects.filter(status='Available')

    if category:
        items = items.filter(procate__iexact=category)
    if query:
        items = items.filter(
            Q(proname__icontains=query) |
            Q(procate__icontains=query) |
            Q(prosubcate__icontains=query) |
            Q(remarks__icontains=query)
        )

    categories = ['Electronics', 'Clothing', 'Furniture', 'Books', 'Other']

    context = {
        'items': items,
        'selected_category': category,
        'search_query': query,
        'categories': categories,
        'is_recipient': bool(request.session.get('recipient_id')),
    }
    return render(request, 'AvailableItems.html', context)


# ==============================================================================
# 3. ITEM REQUEST WORKFLOW
# ==============================================================================

@recipient_required
def RequestItem(request, proid):
    """
    Allows a logged-in recipient to review and request an available item.
    """
    item = get_object_or_404(UnusedThing, proid=proid)
    recipient_id = request.session.get('recipient_id')
    recipient = get_object_or_404(Recipient, recipient_id=recipient_id)

    # 1. Verify item is still Available
    if item.status != 'Available':
        messages.error(request, f"Sorry, '{item.proname}' is no longer available.")
        return redirect('AvailableItems')

    # 2. Check for duplicate pending/approved request by same recipient
    existing_request = DonationRequest.objects.filter(
        recipient=recipient,
        item=item,
        status__in=['Pending', 'Approved']
    ).first()

    if existing_request:
        messages.warning(request, f"You already have a {existing_request.status} request for this item (ID: {existing_request.req_id}).")
        return redirect('MyRequests')

    if request.method == 'POST':
        remarks = request.POST.get('remarks', '').strip()

        # Generate unique Request ID
        count = DonationRequest.objects.count() + 1
        req_id = f"REQ{100 + count}"
        while DonationRequest.objects.filter(req_id=req_id).exists():
            count += 1
            req_id = f"REQ{100 + count}"

        # Create donation request record
        donation_request = DonationRequest(
            req_id=req_id,
            recipient=recipient,
            item=item,
            status='Pending',
            remarks=remarks
        )
        donation_request.save()

        # Update item status to 'Requested' so it is locked from double requests
        with connection.cursor() as cursor:
            cursor.execute("UPDATE unusedthing SET Status = 'Requested' WHERE Proid = %s", [item.proid])

        messages.success(request, f"Your request ({req_id}) for '{item.proname}' has been submitted and is pending administrator approval.")
        return redirect('MyRequests')

    context = {
        'item': item,
        'recipient': recipient,
    }
    return render(request, 'RequestItem.html', context)


@recipient_required
def MyRequests(request):
    """
    Lists all submitted donation requests for the logged-in recipient.
    """
    recipient_id = request.session.get('recipient_id')
    requests_list = DonationRequest.objects.filter(
        recipient__recipient_id=recipient_id
    ).order_by('-req_date', '-req_id')

    return render(request, 'MyRequests.html', {'requests_list': requests_list})


# ==============================================================================
# 4. ADMIN REQUEST MANAGEMENT & DISTRIBUTION WORKFLOW
# ==============================================================================

@admin_required
def AdminRequests(request):
    """
    Administrative overview for managing recipient donation requests.
    """
    status_filter = request.GET.get('status', 'All').strip()

    if status_filter and status_filter != 'All':
        requests_list = DonationRequest.objects.filter(status=status_filter).select_related('recipient').order_by('-req_date', '-req_id')
    else:
        requests_list = DonationRequest.objects.all().select_related('recipient').order_by('-req_date', '-req_id')

    # Count badges
    pending_count = DonationRequest.objects.filter(status='Pending').count()
    approved_count = DonationRequest.objects.filter(status='Approved').count()
    distributed_count = DonationRequest.objects.filter(status='Distributed').count()
    rejected_count = DonationRequest.objects.filter(status='Rejected').count()

    context = {
        'requests_list': requests_list,
        'status_filter': status_filter,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'distributed_count': distributed_count,
        'rejected_count': rejected_count,
    }
    return render(request, 'AdminRequests.html', context)


@admin_required
def ApproveRequest(request, req_id):
    """
    Approves a pending recipient request.
    """
    donation_request = get_object_or_404(DonationRequest, req_id=req_id)

    if donation_request.status == 'Pending':
        donation_request.status = 'Approved'
        donation_request.save()
        messages.success(request, f"Request {req_id} has been Approved. Ready for distribution.")
    else:
        messages.warning(request, f"Request {req_id} cannot be approved because current status is {donation_request.status}.")

    return redirect('AdminRequests')


@admin_required
def RejectRequest(request, req_id):
    """
    Rejects a request and restores the item status back to 'Available'.
    """
    donation_request = get_object_or_404(DonationRequest, req_id=req_id)

    if donation_request.status in ['Pending', 'Approved']:
        donation_request.status = 'Rejected'
        donation_request.save()

        # Restore item to Available so others can request it
        proid = donation_request.item.proid
        with connection.cursor() as cursor:
            cursor.execute("UPDATE unusedthing SET Status = 'Available' WHERE Proid = %s", [proid])

        messages.info(request, f"Request {req_id} has been Rejected. Item {proid} is now Available again.")
    else:
        messages.warning(request, f"Request {req_id} cannot be rejected from status {donation_request.status}.")

    return redirect('AdminRequests')


@admin_required
def DistributeRequest(request, req_id):
    """
    Completes the redistribution workflow:
    1. Marks request status as 'Distributed'
    2. Marks unusedthing status as 'Distributed'
    3. Records distribution in 'distributetable'
    4. Safely updates 'stockdetails' if present
    """
    donation_request = get_object_or_404(DonationRequest, req_id=req_id)

    if donation_request.status != 'Approved':
        messages.warning(request, f"Only Approved requests can be marked as Distributed (current status: {donation_request.status}).")
        return redirect('AdminRequests')

    proid = donation_request.item.proid
    recipient = donation_request.recipient
    admin_name = request.user.username if request.user.is_authenticated else 'Admin'
    today = timezone.now().date()

    # 1. Update DonationRequest status
    donation_request.status = 'Distributed'
    donation_request.save()

    with connection.cursor() as cursor:
        # 2. Update unusedthing status to Distributed
        cursor.execute("UPDATE unusedthing SET Status = 'Distributed' WHERE Proid = %s", [proid])

        # 3. Insert record into distributetable if not already recorded
        cursor.execute("SELECT Proid FROM distributetable WHERE Proid = %s", [proid])
        if not cursor.fetchone():
            cursor.execute("SELECT COALESCE(MAX(Slno), 0) FROM distributetable")
            row = cursor.fetchone()
            next_slno = (row[0] if row and row[0] is not None else 0) + 1

            cursor.execute(
                """INSERT INTO distributetable (Slno, Proid, DisQty, DisDate, DisBy, RecName, RecAdd, RecMob, RecBy, Remarks)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                [
                    next_slno,
                    proid,
                    '1',
                    today,
                    admin_name,
                    recipient.name,
                    f"{recipient.address}, {recipient.city}",
                    recipient.mobile,
                    recipient.name,
                    f"Delivered via Online Request {donation_request.req_id}"
                ]
            )

        # 4. Safe stock update if record exists in stockdetails
        cursor.execute("SELECT Proid FROM stockdetails WHERE Proid = %s", [proid])
        if cursor.fetchone():
            cursor.execute("UPDATE stockdetails SET DisAmt = '1', StockAmt = '0' WHERE Proid = %s", [proid])

    messages.success(request, f"Success! Request {req_id} marked as Distributed. Item '{proid}' successfully logged in Distribution Details.")
    return redirect('AdminRequests')


# ==============================================================================
# 5. SRS OPERATIONAL REPORT VIEWS (ADMIN-ONLY)
# ==============================================================================

@staff_member_required(login_url='/admin/login/')
def ReportHome(request):
    """
    Landing page for SRS Operational Reports.
    Displays core reporting metrics (Total Donations, Beneficiaries Served, Pending Requests)
    and navigation to the 7 operational reports.
    """
    total_donations = UnusedThing.objects.count()

    # Calculate unique beneficiaries served from completed distributions and requests
    dist_recipients = set(DistributeTable.objects.exclude(recname__isnull=True).exclude(recname='').values_list('recname', flat=True))
    req_recipients = set(DonationRequest.objects.filter(status='Distributed').values_list('recipient__name', flat=True))
    beneficiaries_served = len(dist_recipients.union(req_recipients))
    if beneficiaries_served == 0 and DistributeTable.objects.exists():
        beneficiaries_served = DistributeTable.objects.count()

    pending_requests = DonationRequest.objects.filter(status='Pending').count()

    context = {
        'total_donations': total_donations,
        'beneficiaries_served': beneficiaries_served,
        'pending_requests': pending_requests,
        'count_donor': DonorReg.objects.count(),
        'count_unused': UnusedThing.objects.count(),
        'count_collection': CollectionTable.objects.count(),
        'count_stock': StockDetails.objects.count(),
        'count_distribute': DistributeTable.objects.count(),
        'count_complaint': ComplaintTable.objects.count(),
        'count_contact': ContactUs.objects.count(),
    }
    return render(request, 'reports/ReportHome.html', context)


@staff_member_required(login_url='/admin/login/')
def DonorReport(request):
    """
    Displays donor registration records.
    Filters by selected donor or displays all.
    Security: Passwords and hashed fields are strictly omitted.
    """
    selected_filter = request.POST.get('filter_val', 'All') if request.method == 'POST' else 'All'

    if selected_filter and selected_filter != 'All':
        records = DonorReg.objects.filter(donorid=selected_filter).order_by('slno')
    else:
        records = DonorReg.objects.all().order_by('slno')

    all_donors = DonorReg.objects.all().order_by('donorid')
    filter_options = [{'value': d.donorid, 'label': f"{d.dname or d.donorid} ({d.donorid})"} for d in all_donors]

    context = {
        'title': 'Donor Registration Report',
        'records': records,
        'filter_label': 'Donor',
        'filter_options': filter_options,
        'selected_filter': selected_filter,
    }
    return render(request, 'reports/DonorReport.html', context)


@staff_member_required(login_url='/admin/login/')
def UnusedReport(request):
    """
    Displays unused/donated item records from UnusedThing.
    Filters by item category or displays all.
    """
    selected_filter = request.POST.get('filter_val', 'All') if request.method == 'POST' else 'All'

    if selected_filter and selected_filter != 'All':
        records = UnusedThing.objects.filter(procate=selected_filter).order_by('slno')
    else:
        records = UnusedThing.objects.all().order_by('slno')

    raw_cats = UnusedThing.objects.exclude(procate__isnull=True).exclude(procate='').values_list('procate', flat=True).distinct()
    filter_options = [{'value': cat, 'label': cat} for cat in sorted(raw_cats)]

    context = {
        'title': 'Unused Things Report',
        'records': records,
        'filter_label': 'Category',
        'filter_options': filter_options,
        'selected_filter': selected_filter,
    }
    return render(request, 'reports/UnusedReport.html', context)


@staff_member_required(login_url='/admin/login/')
def CollectionReport(request):
    """
    Displays collected items from CollectionTable.
    Filters by product ID or displays all.
    """
    selected_filter = request.POST.get('filter_val', 'All') if request.method == 'POST' else 'All'

    if selected_filter and selected_filter != 'All':
        records = CollectionTable.objects.filter(proid=selected_filter).order_by('slno')
    else:
        records = CollectionTable.objects.all().order_by('slno')

    raw_proids = CollectionTable.objects.values_list('proid', flat=True).distinct()
    filter_options = [{'value': pid, 'label': f"Product {pid}"} for pid in sorted(raw_proids)]

    context = {
        'title': 'Collection Report',
        'records': records,
        'filter_label': 'Product ID',
        'filter_options': filter_options,
        'selected_filter': selected_filter,
    }
    return render(request, 'reports/CollectionReport.html', context)


@staff_member_required(login_url='/admin/login/')
def StockReport(request):
    """
    Displays warehouse stock status from StockDetails.
    Filters by product category or displays all.
    """
    selected_filter = request.POST.get('filter_val', 'All') if request.method == 'POST' else 'All'

    if selected_filter and selected_filter != 'All':
        records = StockDetails.objects.filter(cate=selected_filter).order_by('slno')
    else:
        records = StockDetails.objects.all().order_by('slno')

    raw_cates = StockDetails.objects.exclude(cate__isnull=True).exclude(cate='').values_list('cate', flat=True).distinct()
    filter_options = [{'value': c, 'label': c} for c in sorted(raw_cates)]

    context = {
        'title': 'Stock Details Report',
        'records': records,
        'filter_label': 'Category',
        'filter_options': filter_options,
        'selected_filter': selected_filter,
    }
    return render(request, 'reports/StockReport.html', context)


@staff_member_required(login_url='/admin/login/')
def DistributionReport(request):
    """
    Displays distribution records from DistributeTable.
    Reflects actual recipient details from the distribution workflow.
    Filters by product ID or displays all.
    """
    selected_filter = request.POST.get('filter_val', 'All') if request.method == 'POST' else 'All'

    if selected_filter and selected_filter != 'All':
        records = DistributeTable.objects.filter(proid=selected_filter).order_by('slno')
    else:
        records = DistributeTable.objects.all().order_by('slno')

    raw_proids = DistributeTable.objects.values_list('proid', flat=True).distinct()
    filter_options = [{'value': pid, 'label': f"Product {pid}"} for pid in sorted(raw_proids)]

    context = {
        'title': 'Distribution Details Report',
        'records': records,
        'filter_label': 'Product ID',
        'filter_options': filter_options,
        'selected_filter': selected_filter,
    }
    return render(request, 'reports/DistributionReport.html', context)


@staff_member_required(login_url='/admin/login/')
def ComplaintReport(request):
    """
    Displays complaints and feedback from ComplaintTable.
    Filters by issue type or displays all.
    """
    selected_filter = request.POST.get('filter_val', 'All') if request.method == 'POST' else 'All'

    if selected_filter and selected_filter != 'All':
        records = ComplaintTable.objects.filter(issutype=selected_filter).order_by('slno')
    else:
        records = ComplaintTable.objects.all().order_by('slno')

    raw_types = ComplaintTable.objects.exclude(issutype__isnull=True).exclude(issutype='').values_list('issutype', flat=True).distinct()
    filter_options = [{'value': itype, 'label': itype} for itype in sorted(raw_types)]

    context = {
        'title': 'Complaint & Suggestions Report',
        'records': records,
        'filter_label': 'Issue Type',
        'filter_options': filter_options,
        'selected_filter': selected_filter,
    }
    return render(request, 'reports/ComplaintReport.html', context)


@staff_member_required(login_url='/admin/login/')
def ContactUsReport(request):
    """
    Displays contact us / NGO partner submissions from ContactUs.
    Filters by Organization / Admin ID or displays all.
    """
    selected_filter = request.POST.get('filter_val', 'All') if request.method == 'POST' else 'All'

    if selected_filter and selected_filter != 'All':
        records = ContactUs.objects.filter(admid=selected_filter).order_by('slno')
    else:
        records = ContactUs.objects.all().order_by('slno')

    all_contacts = ContactUs.objects.all().order_by('admid')
    filter_options = [{'value': c.admid, 'label': f"{c.comname or c.admid} ({c.admid})"} for c in all_contacts]

    context = {
        'title': 'Contact Us Report',
        'records': records,
        'filter_label': 'Organization / ID',
        'filter_options': filter_options,
        'selected_filter': selected_filter,
    }
    return render(request, 'reports/ContactUsReport.html', context)
