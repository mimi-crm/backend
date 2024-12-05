import logging

from common.exceptions import (BadRequestException, InternalServerException,
                               UnauthorizedException)
from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from oauth.serializers import LoginSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# 로거 설정
logger = logging.getLogger("custom_api_logger")


# 로그인
class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["Oauth"],
        summary="로그인 API",
        request=LoginSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access_token": {
                        "type": "string",
                        "example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    },
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "전화번호 또는 비밀번호가 잘못되었습니다.",
                    },
                },
            },
        },
    )
    def post(self, request):
        logger.debug(f"로그인 요청 데이터: {request.data}")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.validated_data["tokens"]
            response = Response(
                {
                    "detail": "로그인에 성공했습니다.",
                    "access_token": tokens["access"],
                },
                status=status.HTTP_200_OK,
            )
            # Refresh Token을 쿠키로 저장
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=7 * 24 * 60 * 60,  # 7일
            )
            logger.info(
                f"로그인 성공: 사용자 {request.data.get('username', 'Unknown')}"
            )
            return response
        logger.error(f"로그인 실패: 유효성 검사 오류 {serializer.errors}")
        raise BadRequestException(
            detail="전화번호 또는 비밀번호가 잘못되었습니다.", request=request
        )


# 로그아웃
class LogoutView(APIView):
    """
    로그아웃 API: 액세스 토큰과 리프레시 토큰을 블랙리스트에 추가하고 로그아웃 처리
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Oauth"],
        summary="로그아웃 API",
        description="헤더의 액세스 토큰과 쿠키의 리프레시 토큰을 블랙리스트에 추가 후 로그아웃",
    )
    def post(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("로그아웃 실패: Authorization 헤더가 누락됨")
            raise UnauthorizedException(
                detail="Authorization 헤더에 유효한 액세스 토큰이 없습니다.",
                request=request,
            )

        access_token = auth_header.split(" ")[1]

        try:
            access = AccessToken(access_token)
            user_id = access.get("user_id")
            if not user_id:
                raise UnauthorizedException(
                    detail="유효하지 않은 Access Token입니다.", request=request
                )

            # Refresh Token 캐시에서 가져오기
            refresh_token_key = f"refresh_token:{user_id}"
            refresh_token = cache.get(refresh_token_key)
            if not refresh_token:
                logger.warning(
                    f"로그아웃 실패: Refresh Token 누락 (사용자 ID: {user_id})"
                )
                raise BadRequestException(
                    detail="Refresh Token을 찾을 수 없습니다.", request=request
                )

            # Access Token 블랙리스트에 추가
            try:
                access.blacklist()
            except AttributeError:
                logger.warning("Access Token 블랙리스트 기능이 비활성화됨")

            # Refresh Token 블랙리스트에 추가
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()

            cache.delete(refresh_token_key)

            response = Response(
                {"detail": "로그아웃에 성공했습니다."}, status=status.HTTP_200_OK
            )
            response.delete_cookie("refresh_token")
            logger.info(f"로그아웃 성공: 사용자 ID {user_id}")
            return response

        except Exception as e:
            logger.exception("로그아웃 처리 중 오류 발생")
            raise InternalServerException(
                detail="로그아웃 처리 중 문제가 발생했습니다.", request=request
            )


# 리프레시 토큰 유효성 검사 및 액세스 토큰 재발급
class TokenRefreshView(APIView):
    """
    Access Token 갱신 API
    """

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Oauth"],
        summary="Access Token 갱신",
        description=(
            "만료된 Access Token을 헤더로 보내면, 서버가 쿠키에서 Refresh Token을 가져와 유효성을 검증 후 "
            "새로운 Access Token을 발급합니다."
        ),
    )
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            logger.warning("Access Token 갱신 실패: Refresh Token 누락")
            raise UnauthorizedException(
                detail="Refresh Token이 서버 쿠키에 없습니다.", request=request
            )

        access_token = request.headers.get("Authorization")
        if access_token and access_token.startswith("Bearer "):
            access_token = access_token.split(" ")[1]

        # Access Token 확인
        try:
            AccessToken(access_token)  # Access Token 검증
            logger.info("Access Token 갱신 불필요: Access Token이 아직 유효함")
            return Response(
                {"detail": "Access Token이 아직 유효합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TokenError:
            logger.debug("만료된 Access Token 처리 중...")

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            logger.info("Access Token 갱신 성공")
            return Response(
                {"access_token": new_access_token}, status=status.HTTP_200_OK
            )
        except (TokenError, InvalidToken):
            try:
                invalid_refresh = RefreshToken(refresh_token)
                invalid_refresh.blacklist()
            except AttributeError:
                pass  # 블랙리스트 기능이 비활성화된 경우

            response = Response(
                {"detail": "Refresh Token이 만료되었습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            response.delete_cookie("refresh_token")
            logger.warning(
                "Access Token 갱신 실패: Refresh Token 만료 또는 유효하지 않음"
            )
            return response
