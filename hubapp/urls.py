from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('monitor/', views.monitor, name='monitor'),
    path('search/', views.search, name='search'),
    path('contactus/', views.contactus, name='contactus'),
    path('news/', views.news, name='news'),
    path('permission/', views.permission, name='permission'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('profiles/', views.profiles, name='profiles'),
    path('<int:user_id>/other_profile/', views.other_profile, name='other_profile'),
    path('password/', views.password, name='password'),
    path('<int:user_id>/follow/', views.follow, name='follow'),
    path('<int:user_id>/followerlist/', views.followerlist, name='followerlist'),
    path('<int:user_id>/followinglist/', views.followinglist, name='followinglist'),
]
