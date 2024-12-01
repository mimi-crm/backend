import logging
from pathlib import Path

# 로그 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)  # logs 디렉토리 생성

# 공통 로거 설정
logger = logging.getLogger("custom_api_logger")
logger.setLevel(logging.DEBUG)

# StreamHandler 설정
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# FileHandler 설정 (info.log)
file_handler = logging.FileHandler(LOG_DIR / "info.log")
file_handler.setLevel(logging.INFO)

# FileHandler 설정 (error.log)
error_file_handler = logging.FileHandler(LOG_DIR / "error.log")
error_file_handler.setLevel(logging.ERROR)

# 포매터 설정
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)

# 핸들러를 로거에 추가
if not logger.hasHandlers():
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
