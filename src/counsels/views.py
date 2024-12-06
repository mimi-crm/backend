import logging

from common.exceptions import NotFoundException, UnauthorizedException
from counsels.models import Counsel
from counsels.serializers import CounselDocumentSerializer, CounselSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

# 공통 로거 가져오기
logger = logging.getLogger("custom_api_logger")


@extend_schema(tags=["Counsel"])
class CounselListCreateView(ListCreateAPIView):
    """
    상담 기록 조회 및 생성 API
    """

    serializer_class = CounselSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Counsel"],
        summary="상담 기록 목록 조회",
        description="현재 로그인된 사용자가 소유한 고객의 상담 기록을 조회합니다.",
        responses={
            200: CounselSerializer(many=True),
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Authentication credentials were not provided.",
                    },
                },
            },
        },
    )
    def get(self, request, *args, **kwargs):
        """
        상담 기록 목록 조회
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Counsel"],
        summary="새 상담 기록 생성",
        description="새로운 상담 기록을 생성합니다. 고객은 로그인된 사용자와 연결되어야 합니다.",
        request=CounselSerializer,
        responses={
            201: CounselSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "입력 데이터가 유효하지 않습니다.",
                    },
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "이 고객에 대한 권한이 없습니다.",
                    },
                },
            },
        },
    )
    def post(self, request, *args, **kwargs):
        """
        새 상담 기록 생성
        """
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            raise NotAuthenticated("로그인이 필요합니다.")

        logger.debug(f"상담 기록 조회 요청: 사용자 ID {user.id}")
        return Counsel.objects.filter(customer__user=user)

    def perform_create(self, serializer):
        """
        상담 기록 생성 시, 고객과 연결된 유저를 검증
        """
        customer = serializer.validated_data.get("customer")
        if customer.user != self.request.user:
            logger.warning(
                f"권한 없는 고객 상담 기록 생성 시도: 사용자 ID {self.request.user.id}, 고객 ID {customer.id}"
            )
            raise UnauthorizedException(
                detail="이 고객에 대한 권한이 없습니다.", request=self.request
            )
        serializer.save()
        logger.info(
            f"상담 기록 생성 성공: 사용자 ID {self.request.user.id}, 고객 ID {customer.id}"
        )


@extend_schema(tags=["Counsel"])
class CounselDetailView(RetrieveUpdateDestroyAPIView):
    """
    상담 기록 조회, 수정, 삭제 API
    """

    serializer_class = CounselSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Counsel"],
        summary="상담 기록 상세 조회",
        description="상담 기록의 세부 정보를 조회합니다. 로그인된 사용자와 연결된 고객의 상담 기록만 접근 가능합니다.",
        responses={
            200: CounselSerializer,
            404: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "요청한 상담 기록을 찾을 수 없습니다.",
                    },
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Authentication credentials were not provided.",
                    },
                },
            },
        },
    )
    def get(self, request, *args, **kwargs):
        """
        상담 기록 상세 조회
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Counsel"],
        summary="상담 기록 수정 (전체 업데이트)",
        description="상담 기록의 모든 필드를 수정합니다.",
        request=CounselSerializer,
        responses={
            200: CounselSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "입력 데이터가 유효하지 않습니다.",
                    },
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "요청한 상담 기록을 찾을 수 없습니다.",
                    },
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Authentication credentials were not provided.",
                    },
                },
            },
        },
    )
    def put(self, request, *args, **kwargs):
        """
        상담 기록 수정 (전체 업데이트)
        """
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=["Counsel"],
        summary="상담 기록 수정 (부분 업데이트)",
        description="상담 기록의 일부 필드를 수정합니다.",
        request=CounselSerializer,
        responses={
            200: CounselSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "입력 데이터가 유효하지 않습니다.",
                    },
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "요청한 상담 기록을 찾을 수 없습니다.",
                    },
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Authentication credentials were not provided.",
                    },
                },
            },
        },
    )
    def patch(self, request, *args, **kwargs):
        """
        상담 기록 수정 (부분 업데이트)
        """
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        tags=["Counsel"],
        summary="상담 기록 삭제",
        description="상담 기록을 삭제합니다. 로그인된 사용자와 연결된 고객의 상담 기록만 삭제할 수 있습니다.",
        responses={
            204: {
                "type": "object",
                "description": "삭제 성공 (내용 없음)",
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "요청한 상담 기록을 찾을 수 없습니다.",
                    },
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Authentication credentials were not provided.",
                    },
                },
            },
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        상담 기록 삭제
        """
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            raise NotAuthenticated("로그인이 필요합니다.")

        logger.debug(f"상담 기록 상세 조회 요청: 사용자 ID {user.id}")
        return Counsel.objects.filter(customer__user=user)

    def handle_exception(self, exc):
        """
        커스텀 예외 처리를 적용
        """
        if isinstance(exc, Counsel.DoesNotExist):
            logger.warning(
                f"상담 기록 조회 실패: 상담 기록 ID {self.kwargs.get('pk')}, 사용자 ID {self.request.user.id}"
            )
            raise NotFoundException(
                detail="요청한 상담 기록을 찾을 수 없습니다.", request=self.request
            )
        return super().handle_exception(exc)


@extend_schema(tags=["Counsel-Document"])
class CounselDocumentListCreateView(ListCreateAPIView):
    serializer_class = CounselDocumentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Counsel.objects.all()

    def perform_create(self, serializer):
        """
        새 상담 문서를 생성하고 기존 상담과 연결
        """
        try:
            counsel = serializer.validated_data.get("counsel")

            # 상담이 로그인된 사용자와 연결된 고객의 상담인지 확인
            if counsel.customer.user != self.request.user:
                logger.warning(
                    f"권한 없는 상담 문서 생성 시도: 사용자 ID {self.request.user.id}, 상담 ID {counsel.id}"
                )
                raise ValidationError("이 상담에 대한 권한이 없습니다.")

            # 상담 문서 생성
            serializer.save()
            logger.info(
                f"상담 문서 생성 성공: 사용자 ID {self.request.user.id}, 상담 ID {counsel.id}, 문서 ID {serializer.instance.id}"
            )

        except KeyError as e:
            logger.error("상담 문서 생성 중 필수 필드 누락")
            raise ValidationError(f"필수 데이터가 누락되었습니다: {e}")
        except Exception as e:
            logger.exception("상담 문서 생성 중 오류 발생")
            raise ValidationError("상담 문서 생성 중 문제가 발생했습니다.")
        serializer.save()


@extend_schema(tags=["Counsel-Document"])
class CounselDocumentDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 상담 문서를 조회, 수정, 삭제하는 API
    """

    serializer_class = CounselDocumentSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="상담 문서 조회",
        description="로그인한 사용자가 소유한 특정 상담 문서를 조회합니다.",
        responses={
            200: CounselDocumentSerializer,
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "인증 정보가 제공되지 않았습니다.",
                    },
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "요청한 문서를 찾을 수 없습니다.",
                    },
                },
            },
        },
    )
    def get(self, request, *args, **kwargs):
        """
        특정 상담 문서를 조회합니다.
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="상담 문서 수정",
        description="로그인한 사용자가 소유한 특정 상담 문서를 수정합니다.",
        request=CounselDocumentSerializer,
        responses={
            200: CounselDocumentSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "유효하지 않은 데이터가 제공되었습니다.",
                    },
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "인증 정보가 제공되지 않았습니다.",
                    },
                },
            },
            403: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "이 문서를 수정할 권한이 없습니다.",
                    },
                },
            },
        },
    )
    def put(self, request, *args, **kwargs):
        """
        특정 상담 문서를 수정합니다.
        """
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="상담 문서 삭제",
        description="로그인한 사용자가 소유한 특정 상담 문서를 삭제합니다.",
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
                        "example": "인증 정보가 제공되지 않았습니다.",
                    },
                },
            },
            403: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "이 문서를 삭제할 권한이 없습니다.",
                    },
                },
            },
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        특정 상담 문서를 삭제합니다.
        """
        return super().delete(request, *args, **kwargs)
