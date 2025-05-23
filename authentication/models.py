from uuid import uuid4

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# from .validators import email_exist

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
         raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    username = models.CharField(max_length=100,blank=False,unique=True)
    email = models.EmailField(
        verbose_name='email address',max_length=255,
        unique=True,
    )
    uuid = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    date_created = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
      return self.username
    
    def save(self,**kwargs):
       if self.email:
          return super().save(**kwargs)
       raise ValidationError('Requires an email field')
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    @property
    def full_name(self):
        space = ''
        if self.first_name or self.last_name:
            space = ' '
            return f"{self.first_name}{space}{self.last_name}"
        return self.username
