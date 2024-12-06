from common.constants.choices import GENDER_CHOICES
from django.db import models
from users.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)  # 성별 선택지 제공
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Customer가 생성될 때 CustomerSecurity도 자동 생성
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Customer 저장
        if is_new:  # 새로 생성된 경우만 CustomerSecurity 생성
            CustomerSecurity.objects.create(customer=self)


class CustomerSecurity(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="security"
    )
    is_korean = models.BooleanField(default=True)
    key = models.CharField(max_length=6, default="000000")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
