from email.mime import image
from email.policy import default
from importlib.metadata import requires
from itertools import product
from django.db import models
from django.forms import CharField, ImageField

# Create your models here.
class User(models.Model):
    id = models.CharField(
        max_length=10,
        default=' ',
        primary_key=True,
        null=False,
        )
    name = models.CharField(
        max_length=100,
        null=False,
        )
    avatar = models.ImageField(
        null=False,
        )
    username = models.CharField(
        max_length=100,
        null=False,
    )
    password = models.CharField(
        max_length=100,
        null=False,
    )
    repassword = models.CharField(
        max_length=100,
    )
    permission = models.CharField(
        max_length=10,
        null=False,
    )
    
    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.CharField(
        max_length=10,
        default=' ',
        primary_key=True,
        null=False,
    )
    img =  models.ImageField()
    name = models.CharField(
        max_length=100,
        default=' ',
    )
    category = models.CharField(
        models.ForeignKey("Category", on_delete=models.PROTECT),
        max_length=100, 
        default=' ',
    )
    details = models.CharField(
        max_length=10000,
        default=' ',
    )
    newprice = models.CharField(
        max_length=10,
        default=' ',
    )
    oldprice = models.CharField(
        max_length=10,
        default=' ',
        blank=True,
    )
    count = models.CharField(
        max_length=10,
        default=' ',
    )  
    
    def __str__(self):
        return self.name
    
    def toList(self, cate=None):
        list_return = []
        if cate == None:
            return None
        list_return = list(Product.objects.filter(category=cate.id))
        if list_return.count == 0:
            return None
        return list_return
    
class Category(models.Model):
    id=models.CharField(
        max_length=10,
        default=' ',
        primary_key=True,
        null=False,
    )
    name=models.CharField(
        max_length=100,
        default=' ',
    )  
    
    def __str__(self):
        return self.name
    
    def toList(self):
        return list(Category.objects.all())
    
class Cast(models.Model):
    id=models.CharField(
        max_length=10,
        default=' ',
        primary_key=True,
        null=False,
    )    
    user=models.CharField(
        models.ForeignKey('User', on_delete=models.CASCADE),
        max_length=10,
        default=' ',
    )
    product=models.CharField(
        models.ForeignKey('Product', on_delete=models.CASCADE),
        max_length=10,
        default=' ',
    )
    unit_price=models.CharField(
        models.ForeignKey('Product', on_delete=models.CASCADE),
        max_length=10,
        default=' ',
    )
    amount=models.CharField(
        max_length=5,
        default='1',
    )
    total=models.CharField(
        max_length=15,
        default=' ',
    )
