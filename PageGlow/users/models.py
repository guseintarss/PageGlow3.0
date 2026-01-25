from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True, verbose_name='Фотография')
    data_birth = models.DateTimeField(null=True, blank=True, verbose_name='Дата рождения')
    phone_namber = models.CharField(max_length=11, null=True, blank=True, verbose_name='Номер телефона' )

class Rule(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.key