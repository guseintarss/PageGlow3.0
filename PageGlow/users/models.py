from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True, verbose_name='Фотография')
    data_birth = models.DateTimeField(null=True, blank=True, verbose_name='Дата рождения')
