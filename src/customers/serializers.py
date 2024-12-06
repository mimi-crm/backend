from customers.models import Customer, CustomerSecurity
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "gender",
            "phone_number",
            "address",
            "key",
        ]
        read_only_fields = ["id"]

    @extend_schema_field(serializers.CharField())
    def get_key(self, obj):
        """
        CustomerSecurity의 key를 반환.
        """
        if hasattr(obj, "security"):
            return obj.security.key
        return None

    def create(self, validated_data):
        """
        고객과 CustomerSecurity 생성
        """
        customer = Customer.objects.create(**validated_data)
        CustomerSecurity.objects.create(customer=customer)  # 기본값으로 생성
        return customer


class CustomerSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSecurity
        fields = ["customer", "is_korean", "key"]
