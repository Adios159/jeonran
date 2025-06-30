from typing import List

from .constants import (
    UI_SEPARATOR,
    SAVE_SLOT_COUNT,
    VALID_CONFIRMATION_INPUTS,
)
from .core import SaveSystem
from .exceptions import UserCancelError, InvalidSlotError
from .models import SaveSlotInfo


def show_save_slots(save_system: SaveSystem) -> None:
    """세이브 슬롯 상태를 화면에 표시합니다."""
    print(f"\n{UI_SEPARATOR}")
    print("                💾 세이브 슬롯")
    print(f"{UI_SEPARATOR}")

    slots_info = save_system.get_save_slots_info()
    for slot_num, slot_info in slots_info.items():
        if slot_info is None:
            print(f"슬롯 {slot_num}: [ 비어있음 ]")
        elif isinstance(slot_info, dict) and "error" in slot_info:
            print(f"슬롯 {slot_num}: [ {slot_info['error']} ]")
        elif isinstance(slot_info, SaveSlotInfo):
            print(f"슬롯 {slot_num}: {slot_info}")
            print(f"        저장 시간: {slot_info.save_time}")
    print(f"{UI_SEPARATOR}")


def get_user_slot_choice(
    prompt: str, available_slots: List[int] = None, cancel_allowed: bool = True
) -> int:
    """사용자로부터 슬롯 번호를 입력받습니다."""
    if available_slots:
        print(f"\n사용 가능한 슬롯: {', '.join(map(str, available_slots))}")

    while True:
        try:
            options = f"1-{SAVE_SLOT_COUNT}"
            cancel_prompt = ", 0: 취소" if cancel_allowed else ""
            full_prompt = f"{prompt} ({options}{cancel_prompt}): "
            choice = input(full_prompt).strip()

            if cancel_allowed and choice == "0":
                raise UserCancelError("작업을 취소했습니다.")

            slot_num = int(choice)
            if not (1 <= slot_num <= SAVE_SLOT_COUNT):
                raise InvalidSlotError("슬롯 번호는 1에서 3 사이여야 합니다.")
            
            if available_slots and slot_num not in available_slots:
                print("❗ 선택 가능한 슬롯 번호를 입력해주세요.")
                continue

            return slot_num
        except ValueError:
            print("❗ 숫자를 입력해주세요.")
        except InvalidSlotError as e:
            print(f"❗ {e}")
        except KeyboardInterrupt:
            raise UserCancelError("작업을 취소했습니다.")


def confirm_action(prompt: str) -> bool:
    """사용자에게 특정 작업을 확인받습니다."""
    full_prompt = f"{prompt} (y/n): "
    response = input(full_prompt).strip().lower()
    return response in VALID_CONFIRMATION_INPUTS 