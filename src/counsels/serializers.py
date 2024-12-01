from rest_framework import serializers

from counsels.models import Counsel


class CounselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counsel
        fields = [
            'id',
            'customer',
            'summary',
            'details',
            'emergency',
            'status',
        ]
        read_only_fields = ('id',)

