from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        try:
            # phone_number로 사용자 검색
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("전화번호가 잘못되었습니다.")

        # 비밀번호 검증
        if not check_password(password, user.password):
            raise serializers.ValidationError("비밀번호가 잘못되었습니다.")

        if not user.is_active:
            raise serializers.ValidationError("이 계정은 비활성화 상태입니다.")

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Refresh Token 캐시에 저장
        cache.set(f"refresh_token:{user.id}", refresh_token, timeout=7 * 24 * 60 * 60)  # 7일 만료

        data['tokens'] = {
            'access': access_token,
            'refresh': refresh_token,
        }
        data['user'] = user
        return data
