from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Devices
from .forms import DeviceForm, UserForm
from django.db.models import Q

# Create your views here.

def index(request):
    context = {}
    return render(request, 'hubapp/home.html', context)

def list(request):
    registered_devices = Devices.objects.all()
    return render(request, 'hubapp/list.html', {'registered_devices': registered_devices})

def detail(request, id):
    #Using GET method to retrieve a device
    device = Devices.objects.get(pk=id)
    return render(request, 'hubapp/detail.html', {'device': device})
    
def add(request):
    # Using POST method to submit the form
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        if request.user.is_authenticated:
            newform = DeviceForm()
            return render(request, 'hubapp/add.html', {'form': newform})
        else:
            return redirect('signin')

def edit(request, id):
    # Using GET method to retrieve a device
    dv = Devices.objects.get(pk=id)

    # Using POST method to submit the form
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=dv)
        if form.is_valid():
            form.save()
        return render(request, 'hubapp/edit.html', {'form': form})
    else:
        form = DeviceForm(instance=dv)
    return render(request, 'hubapp/edit.html', {'form': form})

def monitor(request):
    return render(request, 'hubapp/monitor.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = UserForm()
    return render(request, 'hubapp/signup.html', {'form': form})

def signin(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'hubapp/signin.html', {'error': 'Username or password is incorrect.'})
    return render(request, 'hubapp/signin.html')

def signout(request):
    logout(request)
    return redirect('index')

def search(request):
    devices = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        devices = Devices.objects.all().filter(Q(device_name__contains=query) | Q(device_model__contains=query))
    return render(request, 'hubapp/search.html', {'query':query, 'devices':devices})

def contactus(request):
    return render(request, 'hubapp/contactus.html', {})





