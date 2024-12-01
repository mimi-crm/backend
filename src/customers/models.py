from django.db import models

from common.constants.choices import GENDER_CHOICES
from users.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10,  choices=GENDER_CHOICES)  # 성별 선택지 제공
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    key = models.CharField(max_length=6, default="000000")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)