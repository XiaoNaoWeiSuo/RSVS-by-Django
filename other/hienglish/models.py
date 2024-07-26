from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError('The Name field must be set')
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, password, **extra_fields)

class Account(AbstractBaseUser):
    name = models.CharField(max_length=20, unique=True)
    data1 = models.CharField(max_length=1000, blank=True)
    data2 = models.CharField(max_length=1000, blank=True)
    data3 = models.CharField(max_length=1000, blank=True)
    id_front = models.ImageField(upload_to='id_documents/', blank=True, null=True)
    id_back = models.ImageField(upload_to='id_documents/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'name'

    def __str__(self):
        return self.name

from rest_framework.authtoken.models import Token

class AccountToken(Token):
    data1 = models.CharField(max_length=100, blank=True)
    data2 = models.CharField(max_length=100, blank=True)
    data3 = models.CharField(max_length=100, blank=True)

# class PublicAnnouncement(models.Model):
#     s1 = models.CharField(max_length=100, blank=True)
#     s2 = models.CharField(max_length=100, blank=True)
#     s3 = models.CharField(max_length=100, blank=True)
#     l1 = models.CharField(max_length=100, blank=True)
#     l2 = models.CharField(max_length=100, blank=True)
#     l3 = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return f"Public Announcement {self.id}"