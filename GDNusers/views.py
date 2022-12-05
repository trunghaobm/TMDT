from email import contentmanager
from http.client import HTTPResponse
from itertools import count
from operator import mod
from django.utils import timezone
from datetime import date
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
                return redirect('/login')
    
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
def cast(request, userid=None):
    user=models.MyUser().get(id=userid)
    cast=models.Cast().toList(user=userid)
    totalpay=0
    for c in cast:
        totalpay+=int(c.total)
    context ={
        'data' : cast,
        'total': totalpay
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
def pay(request,productid=None):
    msg=[]
    payment=models.Payment().ToList()
    product=models.Product().get(proid=productid)
    if request.method == 'POST':
        paymenid=request.POST.get('delivery')
        if paymenid == 'choose':
            msg.append('Vui lòng chọn hình thức thanh toán!!!')
            pass
        else:
            pay=models.Pay.objects.create(
                user=request.user,
                product=product,
                date=date.today()
            )
            delivery=models.Delivery.objects.create(
                pay = pay,
                method=models.Payment.objects.get(id=paymenid),
                shipper=models.Shipper.objects.get(id=0),
                shippingstatus=models.Shipping.objects.get(id=1)
            )
            context={
                'delivery': delivery
            }
            return redirect('delivery')
    
    context = {
        'user': request.user,
        'product': product,
        'msg': msg,
        'payment': payment
    }
    return render(request, 'access/pay.html', context)

@login_required(login_url='login')
def profile(request, id=None):
    context = {
        'user': request.user
    }
    return render(request, 'access/profile.html', context)

def search(request, key=''):
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

def product(request, id=None):
    context={

    }
    return render(request,'access/product.html', context)

def details(request, product=None):
    pro=models.Product().get(proid=product)
    context={
        'data': pro
    }
    return render(request, 'access/details.html', context)

@login_required
def buy(request, productid=None):
    if request.method == "POST":
        request.method = None
        return redirect('edit')
    pro=models.Product().get(proid=productid)
    context={
        'user': request.user,
        'data': pro,
    }
    return render(request, 'access/buy.html', context)

def edit(request):
    if request.method == 'POST':
        userid = request.user.id
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pid = request.POST.get("pid")
        models.MyUser().update(userid, phone, address)
        request.method = None
        return redirect('buy', pid)
    context={
        'user': request.user,
    }
    return render(request, 'access/edit.html', context)

@login_required
def delivery(request):
    context={
        'data': models.Delivery().ToList(userid=request.user.id)
    }
    return render(request, 'access/delivery.html', context)

@login_required
def deliverydel(request, deliveryid=None):
    models.Delivery().Delete(id=deliveryid)
    return redirect('delivery')
