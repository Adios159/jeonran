import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from .constants import SAVE_SLOT_COUNT, SAVE_FILE_TEMPLATE
from .exceptions import InvalidSlotError, SaveFileError
from .models import SaveSlotInfo


class SaveSystem:
    """게임 저장 및 불러오기 기능을 관리하는 핵심 클래스"""

    def __init__(self, save_dir: str = "."):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def _get_save_file_path(self, slot: int) -> Path:
        """슬롯 번호에 해당하는 세이브 파일 경로를 반환합니다."""
        return self.save_dir / SAVE_FILE_TEMPLATE.format(slot)

    def _validate_slot_number(self, slot: int) -> None:
        """슬롯 번호의 유효성을 검사합니다."""
        if not 1 <= slot <= SAVE_SLOT_COUNT:
            raise InvalidSlotError(f"유효하지 않은 슬롯 번호입니다. (1-{SAVE_SLOT_COUNT})")

    def _read_save_file(self, file_path: Path) -> Dict[str, Any]:
        """세이브 파일을 읽고 내용을 반환합니다."""
        try:
            with file_path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise SaveFileError("파일이 손상되었습니다.")
        except IOError as e:
            raise SaveFileError(f"파일을 읽는 중 오류가 발생했습니다: {e}")

    def _write_save_file(self, file_path: Path, data: Dict[str, Any]) -> None:
        """데이터를 세이브 파일에 씁니다."""
        try:
            with file_path.open('w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise SaveFileError(f"저장 중 오류가 발생했습니다: {e}")

    def get_save_slots_info(self) -> Dict[int, Optional[SaveSlotInfo]]:
        """모든 세이브 슬롯의 정보를 가져옵니다."""
        slots = {}
        for slot in range(1, SAVE_SLOT_COUNT + 1):
            file_path = self._get_save_file_path(slot)
            if not file_path.exists():
                slots[slot] = None
                continue

            try:
                data = self._read_save_file(file_path)
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                slots[slot] = SaveSlotInfo.from_dict(data, mod_time)
            except SaveFileError:
                # UI에서 처리할 수 있도록 None 대신 에러 표시가 가능한 객체나 딕셔너리를 사용할 수도 있습니다.
                # 지금은 None으로 통일하고, get_save_slots에서처럼 처리하겠습니다.
                # 혹은 SaveSlotInfo에 에러 상태를 추가할 수도 있습니다.
                # 여기서는 간단하게 None 처리하고, UI 단에서 파일 존재 여부와 함께 고려합니다.
                # 아니면, 에러 상태를 명시적으로 표현하는 것이 더 좋습니다.
                # get_save_slots 함수는 이제 UI쪽에 가까우니 거기서 에러딕셔너리를 만들고
                # 여기서는 순수하게 정보나 None만 반환하겠습니다.
                slots[slot] = {"error": "파일 손상"} # get_save_slots와 호환성을 위해 유지
        return slots

    def save_game(self, slot: int, player_data: Dict[str, Any]) -> None:
        """게임 상태를 지정된 슬롯에 저장합니다."""
        self._validate_slot_number(slot)
        file_path = self._get_save_file_path(slot)
        self._write_save_file(file_path, player_data)

    def load_game(self, slot: int) -> Dict[str, Any]:
        """지정된 슬롯에서 게임 데이터를 로드합니다."""
        self._validate_slot_number(slot)
        file_path = self._get_save_file_path(slot)
        
        if not file_path.exists():
            raise SaveFileError("해당 슬롯에 저장된 데이터가 없습니다.")
        
        return self._read_save_file(file_path)

    def delete_save(self, slot: int) -> None:
        """지정된 슬롯의 세이브 파일을 삭제합니다."""
        self._validate_slot_number(slot)
        file_path = self._get_save_file_path(slot)
        
        if not file_path.exists():
            # 이미 파일이 없으므로 성공으로 간주하거나, 특정 예외를 발생시킬 수 있습니다.
            # 여기서는 별도 작업을 하지 않습니다.
            return
        
        try:
            file_path.unlink()
        except IOError as e:
            raise SaveFileError(f"파일 삭제 중 오류가 발생했습니다: {e}") 