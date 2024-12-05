from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER,ACCOUNT_TYPE

# Create your models here.

class UserAccountModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER)
    account_no = models.IntegerField(unique=True)
    account_type = models.CharField(max_length=100, choices=ACCOUNT_TYPE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.user.username}-{self.account_no}'

class UserAddressModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='address')
    street_address = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.user.username}-{self.city}'