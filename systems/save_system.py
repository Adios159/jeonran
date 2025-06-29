import json
import os
from datetime import datetime

__all__ = [
    "get_save_slots",
    "show_save_slots",
    "save_game",
    "load_game",
    "delete_save",
    "SaveSystem",
]


def get_save_slots():
    """
    사용 가능한 세이브 슬롯 정보를 반환합니다.
    
    Returns:
        dict: 슬롯 번호와 세이브 정보
    """
    slots = {}
    for i in range(1, 4):  # 슬롯 1, 2, 3
        filename = f"save_data_{i}.json"
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # 파일 수정 시간 확인
                mod_time = os.path.getmtime(filename)
                save_time = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M")
                slots[i] = {
                    "name": data.get("name", "알 수 없음"),
                    "level": data.get("level", 1),
                    "location": data.get("location", "알 수 없음"),
                    "save_time": save_time
                }
            except:
                slots[i] = {"error": "파일 손상"}
        else:
            slots[i] = None
    return slots


def show_save_slots():
    """
    세이브 슬롯 목록을 표시합니다.
    """
    print("\n═══════════════════════════════════════════")
    print("                💾 세이브 슬롯")
    print("═══════════════════════════════════════════")
    
    slots = get_save_slots()
    for slot_num in range(1, 4):
        slot_info = slots[slot_num]
        if slot_info is None:
            print(f"슬롯 {slot_num}: [ 비어있음 ]")
        elif "error" in slot_info:
            print(f"슬롯 {slot_num}: [ 파일 손상 ]")
        else:
            print(f"슬롯 {slot_num}: {slot_info['name']} (Lv.{slot_info['level']}) - {slot_info['location']}")
            print(f"        저장 시간: {slot_info['save_time']}")
    print("═══════════════════════════════════════════")


def save_game(player):
    """
    플레이어 데이터를 선택한 슬롯에 저장합니다.
    
    Args:
        player: Player 객체
    """
    show_save_slots()
    print("\n어느 슬롯에 저장하시겠습니까?")
    
    while True:
        try:
            choice = input("슬롯 번호를 입력하세요 (1-3, 0: 취소): ").strip()
            if choice == "0":
                print("저장을 취소했습니다.")
                return
            
            slot_num = int(choice)
            if slot_num not in [1, 2, 3]:
                print("❗ 1, 2, 3 중에서 선택해주세요.")
                continue
            
            # 기존 세이브가 있는 경우 확인
            filename = f"save_data_{slot_num}.json"
            if os.path.exists(filename):
                confirm = input(f"슬롯 {slot_num}에 이미 데이터가 있습니다. 덮어쓰시겠습니까? (y/n): ").strip().lower()
                if confirm not in ['y', 'yes', '예', 'ㅇ']:
                    continue
            
            # 데이터 저장
            data = {
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
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 슬롯 {slot_num}에 게임이 저장되었습니다!")
            break
            
        except ValueError:
            print("❗ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n저장을 취소했습니다.")
            return


def load_game():
    """
    선택한 슬롯에서 게임 데이터를 불러옵니다.
    
    Returns:
        dict: 저장된 게임 데이터 또는 None
    """
    show_save_slots()
    
    # 저장된 슬롯이 있는지 확인
    slots = get_save_slots()
    available_slots = [i for i in range(1, 4) if slots[i] is not None and "error" not in slots[i]]
    
    if not available_slots:
        print("\n❗ 저장된 파일이 없습니다.")
        return None
    
    print(f"\n사용 가능한 슬롯: {', '.join(map(str, available_slots))}")
    
    while True:
        try:
            choice = input("불러올 슬롯 번호를 입력하세요 (0: 취소): ").strip()
            if choice == "0":
                print("불러오기를 취소했습니다.")
                return None
            
            slot_num = int(choice)
            if slot_num not in available_slots:
                print("❗ 사용 가능한 슬롯 번호를 입력해주세요.")
                continue
            
            filename = f"save_data_{slot_num}.json"
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"📂 슬롯 {slot_num}에서 게임 데이터를 불러왔습니다.")
            return data
            
        except ValueError:
            print("❗ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n불러오기를 취소했습니다.")
            return None
        except Exception as e:
            print(f"❗ 파일을 불러오는 중 오류가 발생했습니다: {e}")
            return None


def delete_save():
    """
    선택한 슬롯의 세이브 파일을 삭제합니다.
    """
    show_save_slots()
    
    # 저장된 슬롯이 있는지 확인
    slots = get_save_slots()
    available_slots = [i for i in range(1, 4) if slots[i] is not None]
    
    if not available_slots:
        print("\n❗ 삭제할 세이브 파일이 없습니다.")
        return
    
    print(f"\n삭제 가능한 슬롯: {', '.join(map(str, available_slots))}")
    
    while True:
        try:
            choice = input("삭제할 슬롯 번호를 입력하세요 (0: 취소): ").strip()
            if choice == "0":
                print("삭제를 취소했습니다.")
                return
            
            slot_num = int(choice)
            if slot_num not in available_slots:
                print("❗ 삭제 가능한 슬롯 번호를 입력해주세요.")
                continue
            
            # 삭제 확인
            slot_info = slots[slot_num]
            if "error" not in slot_info:
                print(f"\n삭제할 데이터: {slot_info['name']} (Lv.{slot_info['level']}) - {slot_info['location']}")
            
            confirm = input("정말로 삭제하시겠습니까? (y/n): ").strip().lower()
            if confirm not in ['y', 'yes', '예', 'ㅇ']:
                print("삭제를 취소했습니다.")
                return
            
            # 파일 삭제
            filename = f"save_data_{slot_num}.json"
            os.remove(filename)
            print(f"🗑️ 슬롯 {slot_num}의 세이브 데이터가 삭제되었습니다.")
            break
            
        except ValueError:
            print("❗ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n삭제를 취소했습니다.")
            return
        except Exception as e:
            print(f"❗ 파일을 삭제하는 중 오류가 발생했습니다: {e}")
            return


class SaveSystem:
    """래퍼 클래스 - 기존 save_game / load_game 함수를 객체 지향적으로 감싸줍니다."""
    def save_game(self, player):
        return save_game(player)
    def load_game(self):
        return load_game() 