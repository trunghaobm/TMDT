from django.contrib import admin
from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('cast/userid=<userid>', views.cast, name='cast'),
    path('pay/castid=<cast>', views.pay, name='pay'),
    path('profile/userid=<id>', views.profile, name='profile'),
    path('search/key=<key>', views.search, name='search'),
    path('manage/', views.manage, name='manage'),
    path('product/id=<id>', views.product, name='product'),
    path('details/product=<product>', views.details, name='details'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)