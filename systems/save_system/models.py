from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

from .constants import (
    DEFAULT_PLAYER_NAME,
    DEFAULT_PLAYER_LEVEL,
    DEFAULT_PLAYER_LOCATION,
    SAVE_TIME_FORMAT
)

@dataclass
class SaveSlotInfo:
    """세이브 슬롯 정보를 담는 데이터 클래스"""
    name: str
    level: int
    location: str
    save_time: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any], save_time: Optional[datetime] = None) -> 'SaveSlotInfo':
        """딕셔너리로부터 SaveSlotInfo 객체 생성"""
        return cls(
            name=data.get("name", DEFAULT_PLAYER_NAME),
            level=data.get("level", DEFAULT_PLAYER_LEVEL),
            location=data.get("location", DEFAULT_PLAYER_LOCATION),
            save_time=save_time.strftime(SAVE_TIME_FORMAT) if save_time else "알 수 없음"
        )

    def __str__(self) -> str:
        """UI 표시용 문자열 반환"""
        return f"{self.name} (Lv.{self.level}) - {self.location}" 