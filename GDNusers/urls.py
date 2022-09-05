from re import T
from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('giohang/', views.GioHang, name='gio hang'),
]
