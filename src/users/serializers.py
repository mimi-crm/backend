import hashlib

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "name",
            "gender",
            "date_of_birth",
            "address",
        ]
        read_only_fields = ("id",)


class UserSignUpSerializer(serializers.ModelSerializer):
    # 비밀번호 필드와 key 필드는 write-only로 설정
    password = serializers.CharField(write_only=True, min_length=8)
    key = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            "phone_number",
            "name",
            "gender",
            "date_of_birth",
            "address",
            "password",  # 비밀번호 필드
            "key",  # key 필드
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "key": {"write_only": True},
        }

    def create(self, validated_data):
        """
        회원가입 로직을 처리하는 메서드.
        - 비밀번호와 key는 해시하여 저장.
        """
        password = validated_data.pop("password")  # 비밀번호 처리
        raw_key = validated_data.pop("key")  # key 처리

        # 사용자 생성
        user = User.objects.create(**validated_data)
        user.set_password(password)  # 비밀번호 해싱 및 저장
        user.key = hashlib.sha256(raw_key.encode()).hexdigest()  # key를 해싱하여 저장
        user.save()  # 사용자 저장
        return user
