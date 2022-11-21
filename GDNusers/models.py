from email.policy import default
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import date
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, name, avatar, username, date_of_birth, address, password=None):
        user = self.model(
            name=name,
            avatar=avatar,
            username=username,
            date_of_birth=date_of_birth,
            address=address
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, avatar, username, date_of_birth, address, password=None):
        user = self.create_user(
            name=name,
            avatar=avatar,
            username=username,
            password=password,
            date_of_birth=date_of_birth,
            address=address,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    name = models.CharField(
        max_length=255,
    )
    avatar = models.ImageField(
        upload_to='images/uploads/avatars',
        blank=True,
    )
    username = models.CharField(
        unique=True,
        max_length=255,
    )
    date_of_birth = models.DateField()
    phone=models.CharField(
        max_length=12,
        null=True,
        blank=True,
    )
    address=models.CharField(
        max_length=1000,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','avatar', 'date_of_birth']

    def __str__(self):
        return self.name

    def get(self, id=None):
        return MyUser.objects.filter(id=id)
    
    def update(self,id, phone, address):
        MyUser.objects.filter(id=id).update(phone=phone, address=address)
        pass
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
   
        
class Category(models.Model):
    id=models.AutoField(
        primary_key=True,
    )
    name=models.CharField(
        max_length=100,
        default=' ',
    )  
    
    def __str__(self):
        return self.name
    
    def toList(self):
        return list(Category.objects.all())
 
class Product(models.Model):
    id=models.AutoField(
        primary_key=True,
    )
    img =  models.ImageField(
        upload_to="images/uploads/products"
    )
    name = models.CharField(
        max_length=100,
        default=' ',
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
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
    
    def get(self, proid=None):
        return Product.objects.get(id=proid)
    
    def toList(self, cate=None):
        return list(Product.objects.filter(category=cate.id))
   
class Cast(models.Model):
    id=models.AutoField(
        primary_key=True,
    )
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    amount=models.CharField(
        max_length=5,
        default='1',
    )
    total=models.CharField(
        max_length=15,
        default=' ',
    )
    
    dateofpayment=models.DateField(
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username+'_cart'
    
    def toList(self, user=None):
        return list(Cast.objects.filter(user=user, dateofpayment=None))
    
class Payment(models.Model):
    id=models.CharField(
        primary_key=True,
        max_length=255
    )
    name=models.CharField(
        max_length=255
    )
    is_using=models.BooleanField()

    def __str__(self):
        return self.name
    
    def Get(self, id=None):
        return Payment.objects.get(id=id)
    
    def ToList(self):
        return list(Payment.objects.all())
       
class Pay(models.Model):
    id=models.AutoField(
        primary_key=True,
    )
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    date=models.DateField(
        default=timezone.now,
        blank=True,
        null=True
    )

    def __str__(self):
        str = 'payid=' + self.id.__str__() + '_'
        str = str + self.user.username + '_'
        str = str + self.product.name.replace(' ','') + '_'
        str = str + self.date.__str__().replace('-','')
        return str

    def toList(self, user=None):
        return list(Pay.objects.filter(user=user.id))

class Shipping(models.Model):
    id=models.CharField(
        max_length=255,
        primary_key=True
    )
    name=models.CharField(
        max_length=255
    )

    def __str__(self) -> str:
        return self.name
    
class Shipper(models.Model):
    id=models.AutoField(
        primary_key=True
    )
    name=models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.name

class Delivery(models.Model):
    id=models.AutoField(
        primary_key=True
    )
    pay=models.ForeignKey(
            Pay, on_delete=models.CASCADE,
            blank=True,
            null=True)
    method=models.ForeignKey(
            Payment, on_delete=models.CASCADE,
            blank=True,
            null=True)
    shipper=models.ForeignKey(
            Shipper, on_delete=models.CASCADE,
            blank=True,
            null=True)
    shippingstatus=models.ForeignKey(
            Shipping, on_delete=models.CASCADE,
            blank=True,
            null=True)

    def __str__(self):
        str = self.id.__str__() + '_'
        str = str + self.pay.__str__() + '_'
        str = str + self.shipper.name
        return str
    
    def ToList(self, userid=None):
        user = MyUser.objects.get(id=userid)
        pay = list(Pay.objects.filter(user=user))
        listret=[]
        for p in pay:
            if p.id==0:
                continue
            listret.extend(list(Delivery.objects.filter(pay=p)))
        return listret

    def Delete(self, id=None):
        Delivery.objects.get(id=id).delete()
