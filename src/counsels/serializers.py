from counsels.models import Counsel, CounselDocument
from rest_framework import serializers


class CounselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counsel
        fields = [
            "id",
            "customer",
            "summary",
            "details",
            "emergency",
            "status",
        ]
        read_only_fields = ("id",)


class CounselDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselDocument
        fields = [
            "id",
            "counsel",
            "summary",
            "document",
            "path",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id",)
