from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from .models import Devices, CustomUser, Activity
from .forms import DeviceForm, UserForm, CustomUserChangeForm, PasswordChangeForm
from django.db.models import Q, F
from django.conf import settings
import requests
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        # My activity feed
        follower_list = Activity.objects.filter(Q(to=request.user) & Q(activity_type='Follower')).order_by('-date')[:3]
        following_list = Activity.objects.filter(Q(creator=request.user) & Q(activity_type='Following')).order_by('-date')[:3]
        new_devices = Devices.objects.filter(user=request.user).order_by('-registered')[:3]
        registered_devices = Devices.objects.filter(last_updated__gt=F('registered'))
        edited_devices = registered_devices.filter(user=request.user).order_by('-last_updated')[:3]
        deleted = Activity.objects.filter(Q(to=request.user) & Q(activity_type='Delete')).order_by('-date')[:3]

        #Following users' activity feed
        followings = request.user.following.all()
        fuser_following_list = Activity.objects.filter(creator__in=followings).order_by('-date')[:3]
        fuser_new_devices = Devices.objects.filter(user__in=followings).order_by('-registered')[:3]
        fuser_registered_devices = Devices.objects.filter(last_updated__gt=F('registered'))
        fuser_edited_devices = fuser_registered_devices.filter(user__in=followings).order_by('-last_updated')[:3]
        fuser_deleted_users = Activity.objects.filter(Q(creator__in=followings) & Q(activity_type='Delete')).order_by('-date')[:3]

        return render(request, 'hubapp/home.html', {'follower_list': follower_list, 'following_list': following_list,
                                                    'new_devices':new_devices, 'edited_devices': edited_devices, 'deleted': deleted,
                                                    'fuser_new_devices':fuser_new_devices, 'fuser_edited_devices': fuser_edited_devices,
                                                    'fuser_deleted_devices': fuser_deleted_users, 'fuser_following_list': fuser_following_list})
    else:
        return render(request, 'hubapp/home.html')

def list(request):
    if request.user.is_authenticated:
        registered_devices = Devices.objects.all()
        return render(request, 'hubapp/list.html', {'registered_devices': registered_devices})
    else:
        return redirect('signin')

def detail(request, id):
    #Using GET method to retrieve a device
    device = Devices.objects.get(pk=id)
    return render(request, 'hubapp/detail.html', {'device': device})
    
def add(request):
    # Using POST method to submit the form
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DeviceForm(request.POST)
            if form.is_valid():
                device = form.save(commit=False)
                device.user = request.user
                device.save()

                add_activity = Activity(
                    creator=request.user,
                    to=request.user,
                    activity_type='Add'
                )
                add_activity.save()
            return render(request, 'hubapp/add.html', {'form': DeviceForm()})
        else:
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

            edit_activity = Activity(
                creator=request.user,
                to=request.user,
                activity_type='Edit'
            )
            edit_activity.save()
        return render(request, 'hubapp/edit.html', {'form': form})
    else:
        form = DeviceForm(instance=dv)
    return render(request, 'hubapp/edit.html', {'form': form})

def delete(request, id):
    # Using GET method to retrieve a device
    dv = Devices.objects.get(pk=id)

    if request.method == 'POST':
        dv.delete()

        delete_activity = Activity(
            creator=request.user,
            to=request.user,
            activity_type='Delete'
        )
        delete_activity.save()
        return redirect('list')
    return render(request, 'hubapp/delete.html', {'dv': dv})

def monitor(request):
    if request.user.is_authenticated:
        return render(request, 'hubapp/monitor.html', {})
    else:
        return redirect('signin')

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
    if request.user.is_authenticated:
        return redirect('myprofile')
    else:
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
        if request.user.is_authenticated:
            query = request.GET.get('q')
            devices = Devices.objects.all().filter(Q(device_name__contains=query) | Q(device_model__contains=query))
        else:
            return render(request, 'hubapp/permission.html')
    return render(request, 'hubapp/search.html', {'query':query, 'devices':devices})

def contactus(request):
    return render(request, 'hubapp/contactus.html', {})

temp_img = "https://images.pexels.com/photos/3225524/pexels-photo-3225524.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500"

def news(request):
    topic = "iot"
    url = "https://newsapi.org/v2/everything?language={}&q={}&sortBy={}&page={}&apiKey={}".format(
         "en", topic, "publishedAt", 1, settings.APIKEY
    )
    r = requests.get(url=url)
    data = r.json()

    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": topic
    }
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description": "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"]
        })
    return render(request, 'hubapp/news.html', context)

def permission(request):
    return render(request, 'hubapp/permission.html', {})

def myprofile(request):
    # My activity feed
    follower_list = Activity.objects.filter(Q(to=request.user) & Q(activity_type='Follower')).order_by('-date')[:3]
    following_list = Activity.objects.filter(Q(creator=request.user) & Q(activity_type='Following')).order_by('-date')[:3]
    new_devices = Devices.objects.filter(user=request.user).order_by('-registered')[:3]
    registered_devices = Devices.objects.filter(last_updated__gt=F('registered'))
    edited_devices = registered_devices.filter(user=request.user).order_by('-last_updated')[:3]
    deleted = Activity.objects.filter(Q(to=request.user) & Q(activity_type='Delete')).order_by('-date')[:3]

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return render(request, 'hubapp/myprofile.html', {'form': form, 'follower_list': follower_list,
                                                         'following_list': following_list, 'new_devices':new_devices,
                                                         'edited_devices': edited_devices, 'deleted': deleted})
    else:
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'hubapp/myprofile.html', {'form': form, 'follower_list': follower_list,
                                                         'following_list': following_list, 'new_devices':new_devices,
                                                         'edited_devices': edited_devices})

def profiles(request):
    if request.user.is_authenticated:
        registered_users = CustomUser.objects.all()
        return render(request, 'hubapp/profiles.html', {'registered_users': registered_users})
    else:
        return redirect('signin')

def other_profile(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(get_user_model(), id=user_id)

        # My activity feed
        follower_list = Activity.objects.filter(Q(to=user) & Q(activity_type='Follower')).order_by('-date')[:3]
        following_list = Activity.objects.filter(Q(creator=user) & Q(activity_type='Following')).order_by('-date')[:3]
        new_devices = Devices.objects.filter(user=user).order_by('-registered')[:3]
        registered_devices = Devices.objects.filter(last_updated__gt=F('registered'))
        edited_devices = registered_devices.filter(user=user).order_by('-last_updated')[:3]
        deleted = Activity.objects.filter(Q(to=user) & Q(activity_type='Delete')).order_by('-date')[:3]

        return render(request, 'hubapp/other_profile.html', {'user': user, 'follower_list': follower_list,
                                                             'following_list': following_list, 'new_devices': new_devices,
                                                             'edited_devices': edited_devices, 'deleted': deleted})
    else:
        return redirect('signin')
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('myprofile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'hubapp/password.html', {'form': form})

def follow(request, user_id):
    requested_user = get_object_or_404(get_user_model(), id=user_id)
    if request.user in requested_user.followers.all():
        requested_user.followedefrs.remove(request.user)
    else:
        requested_user.followers.add(request.user)

    following_activity = Activity(
        creator=request.user,
        to=requested_user,
        activity_type='Following'
    )
    following_activity.save()

    follower_activity = Activity(
        creator=requested_user,
        to=request.user,
        activity_type='Follower'
    )
    follower_activity.save()

    return redirect('profiles')

def followerlist(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    follower_list = user.followers.all()
    return render(request, 'hubapp/followerlist.html', {'follower_list': follower_list})

def followinglist(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    following_list = user.following.all()
    return render(request, 'hubapp/followinglist.html', {'following_list': following_list})


