from pathlib import Path

# 세이브 시스템 기본 설정
SAVE_SLOT_COUNT = 3
SAVE_FILE_TEMPLATE = "save_data_{}.json"
DEFAULT_SAVE_DIR = Path(".")

# UI 관련 상수
VALID_CONFIRMATION_INPUTS = ['y', 'yes', '예', 'ㅇ']
UI_SEPARATOR = "═" * 45

# 기본값 설정
DEFAULT_PLAYER_NAME = "알 수 없음"
DEFAULT_PLAYER_LEVEL = 1
DEFAULT_PLAYER_LOCATION = "알 수 없음"

# 날짜/시간 포맷
SAVE_TIME_FORMAT = "%Y-%m-%d %H:%M" 