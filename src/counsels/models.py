from common.constants.choices import STATUS_CHOICES
from customers.models import Customer
from django.db import models
from users.models import User


class Counsel(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    summary = models.TextField()
    details = models.TextField()
    emergency = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CounselDocument(models.Model):
    counsel = models.ForeignKey(Counsel, on_delete=models.CASCADE)
    summary = models.TextField()
    document = models.FileField(upload_to="documents/%Y/%m/%d")
    path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
