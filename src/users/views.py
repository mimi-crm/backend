import hashlib
import logging

from common.exceptions import BadRequestException, InternalServerException
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.serializers import UserSerializer, UserSignUpSerializer

# 로거 가져오기
logger = logging.getLogger("custom_api_logger")


@extend_schema(tags=["Oauth"], summary="회원가입 API")
class UserSignUpView(CreateAPIView):
    """
    회원가입을 처리하는 View.
    """

    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]  # 회원가입은 인증이 필요 없도록 설정

    def create(self, request, *args, **kwargs):
        """
        회원가입 요청을 처리하는 메서드.
        """
        try:
            logger.debug(f"회원가입 요청 데이터: {request.data}")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # 유효성 검사
            self.perform_create(serializer)  # 사용자 생성
            headers = self.get_success_headers(serializer.data)  # 성공 헤더 추가
            logger.info(f"회원가입 성공: {serializer.data['email']}")
            return Response(
                {
                    "detail": "회원가입이 성공적으로 완료되었습니다.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except ValidationError as e:
            logger.error(f"회원가입 요청 데이터 유효성 검사 실패: {e}")
            raise BadRequestException(
                detail="회원가입 요청 데이터가 유효하지 않습니다.", request=request
            )
        except Exception as e:
            logger.exception("회원가입 중 예기치 못한 오류 발생")
            raise InternalServerException(
                detail="회원가입 처리 중 문제가 발생했습니다.", request=request
            )

    def perform_create(self, serializer):
        """
        사용자를 저장하기 전에 추가 처리를 수행.
        """
        serializer.save()  # 사용자 데이터 저장


@extend_schema(tags=["User-Info"], summary="로그인된 유저의 정보 관리 API")
class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    로그인된 사용자의 정보를 조회, 수정, 삭제하는 View.
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        로그인된 사용자 객체를 반환.
        """
        logger.debug(f"사용자 정보 요청: User ID {self.request.user.id}")
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        비밀번호와 key를 해싱 처리하여 저장.
        """
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            data = request.data.copy()

            # 비밀번호와 key를 해싱 처리
            if "password" in data:
                instance.set_password(data["password"])
                logger.info(f"비밀번호 업데이트 요청: User ID {instance.id}")
                data.pop("password")

            if "key" in data:
                data["key"] = hashlib.sha256(data["key"].encode()).hexdigest()
                logger.info(f"API Key 업데이트 요청: User ID {instance.id}")

            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            logger.info(f"사용자 정보 업데이트 성공: User ID {instance.id}")
            return Response(serializer.data)
        except ValidationError as e:
            logger.error(f"사용자 정보 업데이트 실패 - 유효성 오류: {e}")
            raise BadRequestException(
                detail="사용자 정보가 유효하지 않습니다.", request=request
            )
        except Exception as e:
            logger.exception("사용자 정보 업데이트 중 예기치 못한 오류 발생")
            raise InternalServerException(
                detail="사용자 정보 업데이트 중 문제가 발생했습니다.", request=request
            )

    def delete(self, request, *args, **kwargs):
        """
        로그인된 사용자의 계정을 삭제합니다.
        """
        try:
            user = self.get_object()
            response = super().destroy(request, *args, **kwargs)
            response.data = {"detail": "회원탈퇴에 성공했습니다."}
            logger.info(f"회원탈퇴 성공: User ID {user.id}")
            return response
        except Exception as e:
            logger.exception("회원탈퇴 처리 중 예기치 못한 오류 발생")
            raise InternalServerException(
                detail="회원탈퇴 처리 중 문제가 발생했습니다.", request=request
            )
