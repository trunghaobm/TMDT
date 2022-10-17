from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, name, avatar, username, date_of_birth, password=None):
        user = self.model(
            name=name,
            avatar=avatar,
            username=username,
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, avatar, username, date_of_birth, password=None):
        user = self.create_user(
            name=name,
            avatar=avatar,
            username=username,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    name = models.CharField(
        max_length=255,
        unique=True,
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
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','avatar', 'date_of_birth']

    def __str__(self):
        return self.name

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
