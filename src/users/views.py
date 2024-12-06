import logging

from common.exceptions import BadRequestException, InternalServerException
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer

# 로거 가져오기
logger = logging.getLogger("custom_api_logger")


@extend_schema(tags=["User"])
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class UserCreateView(CreateAPIView):
    """
    회원가입을 처리하는 View.
    """

    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 회원가입은 인증이 필요 없도록 설정

    @extend_schema(
        tags=["Oauth"],
        summary="회원가입 API",
        description="새로운 사용자를 회원가입 처리합니다. 사용자 데이터를 POST 요청으로 전송하면, 회원가입 후 응답으로 사용자 정보를 반환합니다.",
        responses={
            201: UserSerializer,  # 성공적으로 생성된 사용자 데이터 반환
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "회원가입 요청 데이터가 유효하지 않습니다.",
                    },
                },
            },
            500: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "회원가입 처리 중 문제가 발생했습니다.",
                    },
                },
            },
        },
    )
    def post(self, request, *args, **kwargs):
        """
        회원가입 요청을 처리하는 메서드.
        """
        try:
            logger.debug(f"회원가입 요청 데이터: {request.data}")

            # 요청 데이터로 직렬화
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # 유효성 검사

            # 사용자 생성
            user = serializer.save()
            logger.info(f"회원가입 성공: {user.phone_number}")

            # 응답 데이터 준비
            response_data = {
                "detail": "회원가입이 성공적으로 완료되었습니다.",
                "data": {
                    "id": user.id,
                    "phone_number": user.phone_number,
                    "name": user.name,
                    "gender": user.gender,
                    "date_of_birth": user.date_of_birth,
                    "address": user.address,
                },
            }

            # 응답 반환
            return Response(
                response_data,
                status=status.HTTP_201_CREATED,
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


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    로그인된 사용자의 정보를 조회, 수정, 삭제하는 View.
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["User"],
        summary="로그인된 유저 정보 조회",
        description="현재 로그인된 사용자의 정보를 조회합니다.",
        responses={
            200: UserSerializer,
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "인증이 필요합니다.",
                    },
                },
            },
        },
    )
    def get(self, request, *args, **kwargs):
        """
        로그인된 사용자 정보 조회
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["User"],
        summary="로그인된 유저 정보 수정 (전체 업데이트)",
        description="현재 로그인된 사용자의 정보를 수정합니다. 모든 필드를 포함해야 합니다.",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "요청 데이터가 유효하지 않습니다.",
                    },
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "인증이 필요합니다.",
                    },
                },
            },
        },
    )
    def put(self, request, *args, **kwargs):
        """
        로그인된 사용자 정보 수정 (전체 업데이트)
        """
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=["User"],
        summary="로그인된 유저 정보 수정 (부분 업데이트)",
        description="현재 로그인된 사용자의 일부 정보를 수정합니다. 필요한 필드만 요청에 포함하면 됩니다.",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "요청 데이터가 유효하지 않습니다.",
                    },
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "인증이 필요합니다.",
                    },
                },
            },
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        로그인된 사용자 정보 수정 (부분 업데이트)
        """
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["User"],
        summary="로그인된 유저 계정 삭제",
        description="현재 로그인된 사용자의 계정을 삭제합니다. 성공적으로 삭제되면 '회원탈퇴에 성공했습니다.' 메시지를 반환합니다.",
        responses={
            204: {
                "type": "object",
                "description": "삭제 성공 (내용 없음)",
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "인증이 필요합니다.",
                    },
                },
            },
            500: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "회원탈퇴 처리 중 문제가 발생했습니다.",
                    },
                },
            },
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        로그인된 사용자 계정 삭제
        """
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        """
        로그인된 사용자 객체를 반환.
        """
        logger.debug(f"사용자 정보 요청: User ID {self.request.user.id}")
        return self.request.user
