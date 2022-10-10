from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('cast/', views.cast, name='cast'),
    path('pay/', views.pay, name='pay'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('manage/', views.manage, name='manage'),
]