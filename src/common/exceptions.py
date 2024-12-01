from rest_framework.exceptions import APIException
from common.logging_config import logger


class CustomAPIException(APIException):
    """기본 Custom API Exception 클래스"""

    status_code = 400
    default_detail = "요청 처리 중 오류가 발생했습니다."
    default_code = "error"

    def __init__(self, detail=None, code=None, status_code=None, request=None):
        # 상태 코드가 제공되면 재설정
        if status_code:
            self.status_code = status_code

        # 부모 생성자 호출로 detail과 code 설정
        super().__init__(detail=detail or self.default_detail, code=code or self.default_code)

        # 로깅 추가
        if request:
            logger.error(
                f"Error occurred - Path: {request.path}, Method: {request.method}, "
                f"User: {getattr(request, 'user', 'Anonymous')}, Code: {self.code}, Detail: {self.detail}"
            )
        else:
            logger.error(f"Error occurred - Code: {self.code}, Detail: {self.detail}")


class BadRequestException(CustomAPIException):
    """400 Bad Request"""

    status_code = 400
    default_detail = "잘못된 요청입니다."
    default_code = "bad_request"


class NotFoundException(CustomAPIException):
    """404 Not Found"""

    status_code = 404
    default_detail = "리소스를 찾을 수 없습니다."
    default_code = "not_found"


class InternalServerException(CustomAPIException):
    """500 Internal Server Error"""

    status_code = 500
    default_detail = "서버 내부 오류가 발생했습니다."
    default_code = "internal_server_error"


class UnauthorizedException(CustomAPIException):
    """401 Unauthorized"""

    status_code = 401
    default_detail = "인증이 필요합니다."
    default_code = "unauthorized"
