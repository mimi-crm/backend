import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view
from counsels.models import Counsel
from counsels.serializers import CounselSerializer
from common.exceptions import NotFoundException, UnauthorizedException, InternalServerException, BadRequestException

# 공통 로거 가져오기
logger = logging.getLogger("custom_api_logger")


@extend_schema_view(
    get=extend_schema(
        tags=["Counsel"],
        summary="상담 기록 목록 조회",
        description="현재 로그인된 사용자가 소유한 고객의 상담 기록을 조회합니다.",
        responses={
            200: CounselSerializer(many=True),
            401: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Authentication credentials were not provided."},
                },
            },
        },
    ),
    post=extend_schema(
        tags=["Counsel"],
        summary="새 상담 기록 생성",
        description="새로운 상담 기록을 생성합니다. 고객은 로그인된 사용자와 연결되어야 합니다.",
        request=CounselSerializer,
        responses={
            201: CounselSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "입력 데이터가 유효하지 않습니다."},
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "이 고객에 대한 권한이 없습니다."},
                },
            },
        },
    )
)
class CounselListCreateView(ListCreateAPIView):
    """
    상담 기록 조회 및 생성 API
    """
    serializer_class = CounselSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        로그인된 사용자가 소유한 고객의 상담 기록만 반환
        """
        try:
            logger.debug(f"상담 기록 조회 요청: 사용자 ID {self.request.user.id}")
            return Counsel.objects.filter(customer__user=self.request.user)
        except Exception as e:
            logger.exception("상담 기록 조회 중 오류 발생")
            raise InternalServerException(
                detail="상담 기록 조회 중 문제가 발생했습니다.",
                request=self.request
            )

    def perform_create(self, serializer):
        """
        상담 기록 생성 시, 고객과 연결된 유저를 검증
        """
        try:
            customer = serializer.validated_data.get("customer")
            if customer.user != self.request.user:
                logger.warning(f"권한 없는 고객 상담 기록 생성 시도: 사용자 ID {self.request.user.id}, 고객 ID {customer.id}")
                raise UnauthorizedException(detail="이 고객에 대한 권한이 없습니다.", request=self.request)
            serializer.save()
            logger.info(f"상담 기록 생성 성공: 사용자 ID {self.request.user.id}, 고객 ID {customer.id}")
        except ValidationError as e:
            logger.warning(f"상담 기록 생성 유효성 검사 실패: {e}")
            raise BadRequestException(detail="입력 데이터가 유효하지 않습니다.", request=self.request)
        except Exception as e:
            logger.exception("상담 기록 생성 중 오류 발생")
            raise InternalServerException(
                detail="상담 기록 생성 중 문제가 발생했습니다.",
                request=self.request
            )


@extend_schema_view(
    get=extend_schema(
        tags=["Counsel"],
        summary="상담 기록 상세 조회",
        description="상담 기록의 세부 정보를 조회합니다. 로그인된 사용자와 연결된 고객의 상담 기록만 접근 가능합니다.",
        responses={
            200: CounselSerializer,
            404: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "요청한 상담 기록을 찾을 수 없습니다."},
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Authentication credentials were not provided."},
                },
            },
        },
    ),
    put=extend_schema(
        tags=["Counsel"],
        summary="상담 기록 수정 (전체 업데이트)",
        description="상담 기록의 모든 필드를 수정합니다.",
        request=CounselSerializer,
        responses={
            200: CounselSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "입력 데이터가 유효하지 않습니다."},
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "요청한 상담 기록을 찾을 수 없습니다."},
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Authentication credentials were not provided."},
                },
            },
        },
    ),
    patch=extend_schema(
        tags=["Counsel"],
        summary="상담 기록 수정 (부분 업데이트)",
        description="상담 기록의 일부 필드를 수정합니다.",
        request=CounselSerializer,
        responses={
            200: CounselSerializer,
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "입력 데이터가 유효하지 않습니다."},
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "요청한 상담 기록을 찾을 수 없습니다."},
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Authentication credentials were not provided."},
                },
            },
        },
    ),
    delete=extend_schema(
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
                    "detail": {"type": "string", "example": "요청한 상담 기록을 찾을 수 없습니다."},
                },
            },
            401: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string", "example": "Authentication credentials were not provided."},
                },
            },
        },
    )
)
class CounselDetailView(RetrieveUpdateDestroyAPIView):
    """
    상담 기록 조회, 수정, 삭제 API
    """
    serializer_class = CounselSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        로그인된 사용자가 소유한 고객의 상담 기록만 반환
        """
        try:
            logger.debug(f"상담 기록 상세 조회 요청: 사용자 ID {self.request.user.id}")
            return Counsel.objects.filter(customer__user=self.request.user)
        except Exception as e:
            logger.exception("상담 기록 조회 중 오류 발생")
            raise InternalServerException(
                detail="상담 기록을 불러오는 중 문제가 발생했습니다.",
                request=self.request
            )

    def handle_exception(self, exc):
        """
        커스텀 예외 처리를 적용
        """
        if isinstance(exc, Counsel.DoesNotExist):
            logger.warning(f"상담 기록 조회 실패: 상담 기록 ID {self.kwargs.get('pk')}, 사용자 ID {self.request.user.id}")
            raise NotFoundException(detail="요청한 상담 기록을 찾을 수 없습니다.", request=self.request)
        return super().handle_exception(exc)
