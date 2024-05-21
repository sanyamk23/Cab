import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from .models import Customer, Driver, RideRequest
from .forms import CustomerRegistrationForm, DriverRegistrationForm,  RideRequestForm
from django.contrib.auth.decorators import login_required
from geopy.distance import geodesic
from  django.contrib import messages

def home(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'Book a Ride':
            return redirect('customer_login')
        elif action == 'Drive a Ride':
            return redirect('driver_login')
    return render(request, 'home.html')

def customer_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password == password2:
            user = Customer.objects.create(username=username, email=email, password=password)
            return redirect('customer_login')  
        else:
            return render(request, 'customer_register.html', {'error': 'Passwords do not match'})
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer_register.html', {'form': form})

def driver_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        vehicle_number = request.POST['vehicle_number']
        if password == password2:
            user = Driver.objects.create(username=username, email=email, password=password, vehicle_number=vehicle_number)
            return redirect('driver_login')  
        else:
            return render(request, 'driver_register.html', {'error': 'Passwords do not match'})
    else:
        form = DriverRegistrationForm()
    return render(request, 'driver_register.html', {'form': form})

def customer_login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print("Username:", username)
        print("Password:", password)
        try:
            api_key = '55445a6afd3f4afcaac20e4b58c1b925'
            api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + api_key
            
            def get_ip_geolocation_data(ip_address):
                print(ip_address)
                response = requests.get(api_url)
                return response.content
            
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            geolocation_json = get_ip_geolocation_data(ip)
            geolocation_data = json.loads(geolocation_json)
            
            user_latitude = geolocation_data['latitude']
            user_longitude = geolocation_data['longitude']
            # pickup_location = (booking.pickup_latitude, booking.pickup_longitude)
            customer = Customer.objects.get(username=username, password=password)
            customer.latitude = user_latitude
            customer.longitude = user_longitude
            customer.save()
            return redirect('book_cab')
        except Customer.DoesNotExist:
            return HttpResponse("Invalid username or password")
    else:
        return render(request, 'customer_login.html')

def driver_login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print("Username:", username) 
        print("Password:", password) 
        try:
            api_key = '55445a6afd3f4afcaac20e4b58c1b925'
            api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=' + api_key
            
            def get_ip_geolocation_data(ip_address):
                print(ip_address)
                response = requests.get(api_url)
                return response.content
            
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            geolocation_json = get_ip_geolocation_data(ip)
            geolocation_data = json.loads(geolocation_json)
            
            user_latitude = geolocation_data['latitude']
            user_longitude = geolocation_data['longitude']
            driver = Driver.objects.get(username=username, password=password)
            driver.latitude = user_latitude
            driver.longitude = user_longitude
            driver.save()
            return redirect('driver_dashboard')
        except Driver.DoesNotExist:
            return HttpResponse("Invalid username or password")
    else:
        return render(request, 'driver_login.html')


# @login_required
def book_cab(request):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        pickup_location = request.POST.get('pickup_location')
        dropoff_location = request.POST.get('dropoff_location')
        print(customer)
        request.session['customer'] = customer
        request.session['pickup_location'] = pickup_location
        request.session['dropoff_location'] = dropoff_location
        global val
        def val():
            return customer
        ride_request = RideRequest.objects.create(customer=customer, pickup_location=pickup_location, dropoff_location=dropoff_location,status='pending')
        customer_obj = Customer.objects.get(username=customer)
        customer_location = (customer_obj.latitude, customer_obj.longitude)
        max_distance = 2
        send_ride_request_to_drivers(customer_location, max_distance)
        messages.success(request, "Request Generated Successfully") 
        return redirect('waiting_page')
    return render(request, 'book_cab.html')

def generate_ride_request(request):
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride_request = form.save(commit=False)
            ride_request.user = request.user
            ride_request.save()
            return redirect('waiting_page')
    else:
        form = RideRequestForm()
    return render(request, 'generate_ride_request.html', {'form': form})

def send_ride_request_to_drivers(customer_location, max_distance):
    eligible_drivers = []
    active_drivers = Driver.objects.filter(is_available=True)
    for driver in active_drivers:
        driver_location = (driver.latitude, driver.longitude)
        distance = geodesic(customer_location, driver_location).kilometers
        if distance <= max_distance:
            eligible_drivers.append(driver)
    if eligible_drivers:
        pass
    else:
        return render('no_drivers_available.html')

def waiting_page(request):
    try:
        customer_name = request.session['customer']
        customer_pickup = request.session['pickup_location']
        customer_dropoff = request.session['dropoff_location']
        print(customer_name)

        ride = RideRequest.objects.get(customer=customer_name, pickup_location=customer_pickup, dropoff_location=customer_dropoff)
        print(ride.id)
        ride_id = ride.id
        ride_request = RideRequest.objects.get(id=ride_id, customer=customer_name, pickup_location=customer_pickup, dropoff_location=customer_dropoff)

        return render(request, 'waiting.html', {'ride_request':ride_request})
    except RideRequest.MultipleObjectsReturned:
        RideRequest.objects.filter(customer=customer_name, pickup_location=customer_pickup, dropoff_location=customer_dropoff).delete()
        return render(request, 'too_many_rides.html')

def driver_dashboard(request):
    if request.method == 'POST':
        ride_request_id = request.POST.get('ride_request_id')
        ride_request = RideRequest.objects.get(pk=ride_request_id)
        ride_request.status = 'accepted'
        ride_request.save()
        return redirect('accepted', ride_request_id=ride_request_id) 
    ride_requests = RideRequest.objects.filter(status='pending')
    new_request_generated = ride_requests.exists()
    ride_request1 = RideRequest.objects.filter(status='rejected')
    return render(request, 'driver_dashboard.html', {'ride_requests': ride_requests, 'new_request_generated': new_request_generated, 'ride_request1': ride_request1})

def accept_ride_request(request, ride_request_id):
    ride_request = RideRequest.objects.get(pk=ride_request_id)
    ride_request.status = RideRequest.STATUS_ACCEPTED
    ride_request.save()
    return render(request, 'accepted.html', {'ride_request_id': ride_request_id, 'ride_request': ride_request})

def reject_ride_request(request, ride_request_id):
    ride_request = RideRequest.objects.get(pk=ride_request_id)
    ride_request.status = RideRequest.STATUS_REJECTED
    ride_request.save()
    return redirect('driver_dashboard')

def accepted_page(request):
    return render(request, 'accepted_page.html')

def rejected_page(request):
    return render(request, 'rejected_page.html')

def accepted(request, ride_request_id):
    return render(request, 'accepted.html', {'ride_request_id': ride_request_id})