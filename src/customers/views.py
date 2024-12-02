import logging

from common.exceptions import (BadRequestException, InternalServerException,
                               NotFoundException)
from customers.models import Customer
from customers.serializers import CustomerSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# 공통 로거 가져오기
logger = logging.getLogger("custom_api_logger")


@extend_schema_view(
    get=extend_schema(
        tags=["Customer"],
        summary="고객 목록 조회",
        description="현재 로그인된 사용자의 모든 고객을 조회합니다.",
        responses={
            200: CustomerSerializer(many=True),
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
    ),
    post=extend_schema(
        tags=["Customer"],
        summary="새 고객 생성",
        description="새로운 고객 정보를 생성합니다. 생성된 고객은 현재 로그인된 사용자와 연결됩니다.",
        request=CustomerSerializer,
        responses={
            201: CustomerSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Invalid data."},
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
    ),
)
class CustomerListCreateView(generics.ListCreateAPIView):
    """
    고객 목록 조회 및 새 고객 생성 API
    """

    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        현재 로그인된 사용자와 연결된 고객만 반환
        """
        try:
            logger.debug(f"고객 목록 조회 요청: 사용자 ID {self.request.user.id}")
            return Customer.objects.filter(user=self.request.user)
        except Exception as e:
            logger.exception("고객 목록 조회 중 예기치 못한 오류 발생")
            raise InternalServerException(
                detail="고객 목록을 불러오는 중 문제가 발생했습니다.",
                request=self.request,
            )

    def perform_create(self, serializer):
        """
        새 고객을 생성할 때 현재 로그인된 사용자를 설정
        """
        try:
            logger.debug(f"새 고객 생성 요청 데이터: {serializer.validated_data}")
            serializer.save(user=self.request.user)
            logger.info(
                f"새 고객 생성 성공: 사용자 ID {self.request.user.id}, 고객 ID {serializer.instance.id}"
            )
        except Exception as e:
            logger.exception("고객 생성 중 예기치 못한 오류 발생")
            raise InternalServerException(
                detail="고객 생성 중 문제가 발생했습니다.", request=self.request
            )


@extend_schema_view(
    get=extend_schema(
        tags=["Customer"],
        summary="특정 고객 조회",
        description="현재 로그인된 사용자가 소유한 특정 고객의 상세 정보를 조회합니다.",
        responses={
            200: CustomerSerializer,
            404: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Not found."},
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
    ),
    put=extend_schema(
        tags=["Customer"],
        summary="특정 고객 정보 수정 (전체 업데이트)",
        description="현재 로그인된 사용자가 소유한 특정 고객의 모든 필드를 업데이트합니다.",
        request=CustomerSerializer,
        responses={
            200: CustomerSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Invalid data."},
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Not found."},
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
    ),
    patch=extend_schema(
        tags=["Customer"],
        summary="특정 고객 정보 수정 (부분 업데이트)",
        description="현재 로그인된 사용자가 소유한 특정 고객의 일부 필드를 업데이트합니다.",
        request=CustomerSerializer,
        responses={
            200: CustomerSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Invalid data."},
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Not found."},
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
    ),
    delete=extend_schema(
        tags=["Customer"],
        summary="특정 고객 삭제",
        description="현재 로그인된 사용자가 소유한 특정 고객을 삭제합니다.",
        responses={
            204: {
                "type": "object",
                "description": "삭제 성공 (내용 없음)",
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Not found."},
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
    ),
)
class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    특정 고객 조회, 수정, 삭제 API
    """

    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        현재 로그인된 사용자와 연결된 특정 고객만 조회 가능
        """
        try:
            return Customer.objects.filter(user=self.request.user)
        except Exception as e:
            logger.exception("고객 조회 중 예기치 못한 오류 발생")
            raise InternalServerException(
                detail="고객 정보를 불러오는 중 문제가 발생했습니다.",
                request=self.request,
            )

    def handle_exception(self, exc):
        """
        NotFoundException과 같은 커스텀 예외 처리를 수행
        """
        if isinstance(exc, Customer.DoesNotExist):
            logger.warning(
                f"고객 정보 조회 실패: 고객 ID {self.kwargs.get('pk')}, 사용자 ID {self.request.user.id}"
            )
            raise NotFoundException(
                detail="요청한 고객을 찾을 수 없습니다.", request=self.request
            )
        return super().handle_exception(exc)
