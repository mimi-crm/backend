from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from common.constants.choices import GENDER_CHOICES


class UserManager(BaseUserManager):
    # 사용자 생성을 담당하는 메서드
    def create_user(
        self,
        phone_number,
        name,
        gender,
        date_of_birth,
        address,
        password=None,
        **kwargs,
    ):
        # 전화번호가 없는 경우 예외 발생
        if not phone_number:
            raise ValueError("Users must have a phone number")

        # 사용자 계정을 기본적으로 활성화 상태로 설정
        kwargs.setdefault("is_active", True)

        # User 모델의 인스턴스를 생성
        user = self.model(
            phone_number=phone_number,
            name=name,
            gender=gender,
            date_of_birth=date_of_birth,
            address=address,
            **kwargs,
        )

        # 비밀번호가 주어진 경우 설정하고, 그렇지 않으면 비밀번호 설정을 사용 불가로 지정
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        # 데이터베이스에 사용자 저장
        user.save(using=self._db)
        return user

    # 관리자 계정(슈퍼유저) 생성을 위한 메서드
    def create_superuser(self, phone_number, password, **kwargs):
        # 관리자 계정의 기본 속성 설정 (활성화, 스태프, 슈퍼유저 권한)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_staff", True)

        # 전화번호가 없는 경우 예외 발생
        if not phone_number:
            raise ValueError("Superusers must have a phone number")

        # 슈퍼유저 생성. 기본적으로 이름, 성별, 생년월일, 주소 등의 값을 제공
        user = self.create_user(
            phone_number=phone_number,
            name=kwargs.get('name', 'Admin'),  # 기본 이름을 'Admin'으로 설정 (제공되지 않은 경우)
            gender=kwargs.get('gender', 'Other'),  # 기본 성별을 'Other'로 설정 (제공되지 않은 경우)
            date_of_birth=kwargs.get('date_of_birth', '2000-01-01'),  # 기본 생년월일 설정 (제공되지 않은 경우)
            address=kwargs.get('address', 'No address'),  # 기본 주소 설정 (제공되지 않은 경우)
            password=password,
            **kwargs
        )

        return user


# 사용자 모델 정의
class User(AbstractBaseUser, PermissionsMixin):
    # 사용자 모델 필드 정의
    phone_number = models.CharField(max_length=13, unique=True)  # 전화번호를 유일하게 사용
    password = models.CharField(max_length=128,)
    key = models.CharField(max_length=128, default="000000")
    name = models.CharField(max_length=25)  # 사용자 이름
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES  # 성별 선택지 제공
    )
    date_of_birth = models.DateField()  # 생년월일
    address = models.CharField(max_length=255)  # 사용자 주소
    is_active = models.BooleanField(default=True)  # 계정 활성 상태
    is_staff = models.BooleanField(default=False)  # 스태프 권한 여부 (관리자 페이지 접근 가능 여부)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 인증에 사용할 필드를 설정. 전화번호로 로그인 가능
    USERNAME_FIELD = "phone_number"
    # 필수 필드 설정 (관리자 생성 시 요구됨)
    REQUIRED_FIELDS = ['name', 'gender', 'date_of_birth', 'address']

    # 사용자 관리자 연결
    objects = UserManager()

