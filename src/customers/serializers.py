from rest_framework import serializers

from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
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