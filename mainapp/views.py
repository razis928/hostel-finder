from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import *

def check_availability(request):
    email = request.GET.get('email', None)
    username = request.GET.get('username', None)
    data = {}

    if email:
        if User.objects.filter(email=email).exists():
            data['email_exists'] = True
        else:
            data['email_exists'] = False

    if username:
        if User.objects.filter(username=username).exists():
            data['username_exists'] = True
        else:
            data['username_exists'] = False

    return JsonResponse(data)

def index(request):
    first_letter = ''
    room_count = ''
    customer = ''
    if request.user.is_authenticated:
        first_letter = request.user.username[0]
        customer = Customer.objects.get(user=request.user)
    hostels = Hostel.objects.all()[:3]
    for hostel in hostels:
        room_count = Room.objects.filter(hostel=hostel).count()
    
    return render(request, 'index.html', {'first_letter':first_letter, 'hostels':hostels, 'room_count':room_count, 'customer':customer})

def about(request):
    first_letter = ''
    customer = ''
    if request.user.is_authenticated:
        first_letter = request.user.username[0]
        customer = Customer.objects.get(user=request.user)
    
    return render(request, 'about.html', {'first_letter':first_letter, 'customer':customer})

def terms_conditions(request):
    first_letter = ''
    customer = ''
    if request.user.is_authenticated:
        first_letter = request.user.username[0]
        customer = Customer.objects.get(user=request.user)
    
    return render(request, 'terms.html', {'first_letter':first_letter, 'customer':customer})

def all_hostels(request):
    first_letter = ''
    room_count = ''
    customer = ''
    if request.user.is_authenticated:
        first_letter = request.user.username[0]
        customer = Customer.objects.get(user=request.user)

    # Get the area filter from the request
    area = request.GET.get('area', None)

    # Filter hostels based on the selected area if provided
    if area:
        hostels = Hostel.objects.filter(area=area)
    else:
        hostels = Hostel.objects.all()

    # Count rooms for each hostel (if needed in the template)
    for hostel in hostels:
        room_count = Room.objects.filter(hostel=hostel).count()

    return render(request, 'property-list.html', {'first_letter': first_letter, 'hostels': hostels, 'room_count': room_count, 'customer':customer})

def hostel_list(request):
    first_letter = ''
    customer = ''
    if request.user.is_authenticated:
        first_letter = request.user.username[0]
        customer = Customer.objects.get(user=request.user)
    area = request.GET.get('area')
    if area:
        hostels = Hostel.objects.filter(area=area)
    else:
        hostels = Hostel.objects.all()
    for hostel in hostels:
        room_count = Room.objects.filter(hostel=hostel).count()
    
    context = {
        'hostels': hostels,
        'first_letter': first_letter,
        'customer': customer,
        'room_count': room_count
    }
    return render(request, 'hostel_list.html', context)

def hostel_detail(request, pk):
    first_letter = ''
    customer = ''
    if request.user.is_authenticated:
        first_letter = request.user.username[0]
        customer = Customer.objects.get(user=request.user)
    hostel = Hostel.objects.get(id=pk)
    rooms = hostel.rooms.all()
    return render(request, 'single-hostel.html', {'hostel':hostel, 'first_letter':first_letter, 'rooms':rooms, 'customer':customer})

@login_required
def profile(request):
    first_letter = ''
    if request.user.is_authenticated:
        first_letter = request.user.username[0]
    user = request.user
    customer = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_profile_picture', customer.profile_picture)
        first_name = request.POST.get('profile_first_name')
        last_name = request.POST.get('profile_last_name')
        username = request.POST.get('profile_username')
        email = request.POST.get('profile_email')
        phone = request.POST.get('profile_phone_number')
        address = request.POST.get('profile_address')

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email    
        user.save()
    
        customer.phone = phone
        customer.address = address
        customer.profile_picture = profile_picture
        customer.save()

    return render(request, 'profile.html', {'first_letter':first_letter, 'customer':customer})

def contact(request):
    first_letter = ''
    customer = ''
    if request.user.is_authenticated:
        first_letter = request.user.username[0]
        customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        name = request.POST.get('c_name')
        email = request.POST.get('c_email')
        subject = request.POST.get('c_subject')
        message = request.POST.get('c_message')

        Contact.objects.create(name=name, email=email, subject=subject, message=message)

        return redirect('/contact')
    return render(request, 'contact.html', {'first_letter':first_letter, 'customer':customer})

def hostel_owner_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('hor_firstName')
        last_name = request.POST.get('hor_lastName')
        username = request.POST.get('hor_userName')
        email = request.POST.get('hor_email')
        phone = request.POST.get('hor_phone')
        address = request.POST.get('hor_address')
        password = request.POST.get('hor_password')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = True
        user.save()

        hostel_owner = HostelOwner()
        hostel_owner.user = user
        hostel_owner.phone_number = phone
        hostel_owner.address = address
        hostel_owner.save()

        return redirect('/login')
    return render(request, 'owner_register.html')

def customer_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('cr_firstName')
        last_name = request.POST.get('cr_lastName')
        username = request.POST.get('cr_userName')
        email = request.POST.get('cr_email')
        phone = request.POST.get('cr_phone')
        address = request.POST.get('cr_address')
        password = request.POST.get('cr_password')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        customer = Customer()
        customer.user = user
        customer.phone_number = phone
        customer.address = address
        customer.save()

        return redirect('/login')
    return render(request, 'customer_register.html')

def user_logout(request):
    logout(request)
    return redirect('/') 

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('loginuserName')
        password = request.POST.get('loginpassword')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('/')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
