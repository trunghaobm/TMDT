from email import contentmanager
from itertools import count
from operator import mod
from tkinter.messagebox import RETRY
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from . import models

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+ user)
                return redirect('users/login')
    
        context = {'form' : form}
        return render(request, 'users/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:    
                messages.info(request, 'username or password incorect')
        context = {}
        return render(request, 'users/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def cast(request):
    context ={
        'data' : list(range(10)),
        'count': 1,
    }
    return render(request, 'access/cast.html', context)

def home(request):
    catelist = {}
    catename = models.Category().toList()
    products =[]
    for cate in catename:
        products = models.Product().toList(cate=cate)
        catelist[cate] = products
    #endfor
    context ={
        'categories' : catelist,
    }
    return render(request, 'access/home.html', context)

@login_required(login_url='login')
def pay(request):
    context = {
        
    }
    return render(request, 'access/pay.html', context)

@login_required(login_url='login')
def profile(request):
    context = {
        
    }
    return render(request, 'access/profile.html', context)

def search(request):
    cate = models.Category().toList()
    context = {
        'categories' : cate,
    }
    return render(request, 'access/search.html', context)

@permission_required('administrator', login_url='login')
def manage(request):
    cate = models.Category().toList()
    context = {
        'categories' : cate,
    }
    return render(request, 'admin/manage.html', context)