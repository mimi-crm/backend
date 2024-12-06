import logging

from common.exceptions import (InternalServerException, NotFoundException,
                               UnauthorizedException)
from customers.models import Customer, CustomerSecurity
from customers.serializers import (CustomerSecuritySerializer,
                                   CustomerSerializer)
from drf_spectacular.utils import extend_schema
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

# 공통 로거 가져오기
logger = logging.getLogger("custom_api_logger")


class CustomerListCreateView(ListCreateAPIView):
    """
    고객 목록 조회 및 새 고객 생성 API
    """

    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
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
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
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
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomerDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 고객 조회, 수정, 삭제 API
    """

    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
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
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
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
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
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
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
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
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@extend_schema(tags=["Customer"])
class CustomerSecurityEditView(RetrieveUpdateAPIView):
    """
    특정 고객의 보안 정보를 조회 및 수정하는 API
    """

    serializer_class = CustomerSecuritySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        customer_id = self.kwargs.get("pk")
        return CustomerSecurity.objects.filter(customer__id=customer_id)

    @extend_schema(
        tags=["Customer"],
        summary="특정 고객의 보안 정보 조회",
        description="특정 고객의 보안 정보를 조회합니다.",
        responses={
            200: CustomerSecuritySerializer,
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
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=["Customer"],
        summary="특정 고객의 보안 정보 수정",
        description="특정 고객의 보안 정보를 수정합니다.",
        request=CustomerSecuritySerializer,
        responses={
            200: CustomerSecuritySerializer,
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
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
