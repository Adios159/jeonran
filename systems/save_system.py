from typing import Any, Dict

from .save_system.core import SaveSystem
from .save_system.ui import show_save_slots, get_user_slot_choice, confirm_action
from .save_system.exceptions import SaveSystemError, UserCancelError


__all__ = [
    "get_save_slots",
    "show_save_slots_legacy", # 이름 변경
    "save_game",
    "load_game",
    "delete_save",
    "SaveSystemWrapper", # 이름 변경
]

# 전역 SaveSystem 인스턴스
_save_system = SaveSystem()


def get_save_slots() -> Dict[int, Any]:
    """
    사용 가능한 세이브 슬롯 정보를 반환합니다. (레거시 호환용)
    """
    return _save_system.get_save_slots_info()


def show_save_slots_legacy():
    """
    세이브 슬롯 목록을 표시합니다.
    """
    show_save_slots(_save_system)


def save_game(player: Any):
    """
    플레이어 데이터를 선택한 슬롯에 저장합니다.
    """
    show_save_slots(_save_system)
    
    try:
        slot_num = get_user_slot_choice("어느 슬롯에 저장하시겠습니까?")
        
        slots_info = _save_system.get_save_slots_info()
        if slots_info.get(slot_num) is not None:
            if not confirm_action(f"슬롯 {slot_num}에 이미 데이터가 있습니다. 덮어쓰시겠습니까?"):
                print("저장을 취소했습니다.")
                return

        player_data = {
            "name": player.name,
            "job": player.job,
            "level": player.level,
            "exp": player.exp,
            "hp": player.hp,
            "mp": player.mp,
            "inventory": player.inventory,
            "location": player.location,
            "status_effects": player.status_effects,
        }
        
        _save_system.save_game(slot_num, player_data)
        print(f"💾 슬롯 {slot_num}에 게임이 저장되었습니다!")

    except (SaveSystemError, UserCancelError) as e:
        print(f"❗ {e}")
    except Exception as e:
        print(f"❗ 예상치 못한 오류가 발생했습니다: {e}")


def load_game() -> Dict[str, Any] | None:
    """
    선택한 슬롯에서 게임 데이터를 불러옵니다.
    """
    show_save_slots(_save_system)
    
    slots_info = _save_system.get_save_slots_info()
    available_slots = [
        s for s, info in slots_info.items() if info is not None
    ]

    if not available_slots:
        print("\n❗ 저장된 파일이 없습니다.")
        return None

    try:
        slot_num = get_user_slot_choice("불러올 슬롯 번호를 입력하세요", available_slots)
        data = _save_system.load_game(slot_num)
        print(f"📂 슬롯 {slot_num}에서 게임 데이터를 불러왔습니다.")
        return data
    except (SaveSystemError, UserCancelError) as e:
        print(f"❗ {e}")
        return None
    except Exception as e:
        print(f"❗ 예상치 못한 오류가 발생했습니다: {e}")
        return None


def delete_save():
    """
    선택한 슬롯의 세이브 파일을 삭제합니다.
    """
    show_save_slots(_save_system)

    slots_info = _save_system.get_save_slots_info()
    available_slots = [
        s for s, info in slots_info.items() if info is not None
    ]

    if not available_slots:
        print("\n❗ 삭제할 세이브 파일이 없습니다.")
        return

    try:
        slot_num = get_user_slot_choice("삭제할 슬롯 번호를 입력하세요", available_slots)

        slot_info = slots_info[slot_num]
        if isinstance(slot_info, dict) and "error" in slot_info:
             print(f"\n삭제할 데이터: [ 파일 손상 ]")
        else:
            print(f"\n삭제할 데이터: {slot_info}")

        if not confirm_action("정말로 삭제하시겠습니까?"):
            print("삭제를 취소했습니다.")
            return

        _save_system.delete_save(slot_num)
        print(f"🗑️ 슬롯 {slot_num}의 세이브 데이터가 삭제되었습니다.")

    except (SaveSystemError, UserCancelError) as e:
        print(f"❗ {e}")
    except Exception as e:
        print(f"❗ 예상치 못한 오류가 발생했습니다: {e}")


class SaveSystemWrapper:
    """래퍼 클래스 - 새로운 SaveSystem 모듈을 사용하도록 업데이트되었습니다."""
    def save_game(self, player: Any):
        return save_game(player)

    def load_game(self) -> Dict[str, Any] | None:
        return load_game() 