import json
import copy
from typing import Dict, List, Optional, Tuple


class QuestSystem:
    """
    조선시대 RPG 퀘스트 시스템
    
    퀘스트 타입:
    - kill: 몬스터 처치 퀘스트
    - collect: 아이템 수집 퀘스트  
    - travel: 지역 이동 퀘스트
    """
    
    def __init__(self):
        self.quests_data = {}           # 모든 퀘스트 템플릿
        self.player_quests = {}         # 플레이어의 퀘스트 진행 상황
        self.completed_quests = set()   # 완료된 퀘스트 ID들
        self.load_quests_data()
    
    def load_quests_data(self):
        """퀘스트 데이터 파일 로드"""
        try:
            with open("data/quests.json", "r", encoding="utf-8") as f:
                quests_list = json.load(f)
            
            # 리스트를 딕셔너리로 변환 (ID를 키로 사용)
            self.quests_data = {quest["id"]: quest for quest in quests_list}
            
        except FileNotFoundError:
            print("❗ 퀘스트 데이터 파일을 찾을 수 없습니다.")
            self.quests_data = {}
        except json.JSONDecodeError:
            print("❗ 퀘스트 데이터 파일 형식이 올바르지 않습니다.")
            self.quests_data = {}
    
    def get_available_quests(self, player_level: int, player_region: str) -> List[Dict]:
        """
        현재 수락 가능한 퀘스트 목록 반환
        
        Args:
            player_level: 플레이어 레벨
            player_region: 플레이어 현재 지역
            
        Returns:
            List[Dict]: 수락 가능한 퀘스트 목록
        """
        available = []
        
        for quest_id, quest_data in self.quests_data.items():
            # 이미 완료되었거나 진행 중인 퀘스트는 제외
            if quest_id in self.completed_quests or quest_id in self.player_quests:
                continue
            
            # 퀘스트 지역과 플레이어 지역이 같은지 확인
            if quest_data["region"] != player_region:
                continue
            
            # 레벨 조건 확인
            if player_level < quest_data["requirements"]["min_level"]:
                continue
            
            # 선행 퀘스트 완료 여부 확인
            required_quests = quest_data["requirements"]["completed_quests"]
            if not all(req_id in self.completed_quests for req_id in required_quests):
                continue
            
            available.append(quest_data)
        
        return available
    
    def accept_quest(self, quest_id: str) -> bool:
        """
        퀘스트 수락
        
        Args:
            quest_id: 퀘스트 ID
            
        Returns:
            bool: 수락 성공 여부
        """
        if quest_id not in self.quests_data:
            return False
        
        if quest_id in self.player_quests or quest_id in self.completed_quests:
            return False
        
        # 퀘스트 데이터 복사하여 플레이어 퀘스트에 추가
        quest_copy = copy.deepcopy(self.quests_data[quest_id])
        quest_copy["status"] = "active"
        self.player_quests[quest_id] = quest_copy
        
        return True
    
    def abandon_quest(self, quest_id: str) -> bool:
        """
        퀘스트 포기
        
        Args:
            quest_id: 퀘스트 ID
            
        Returns:
            bool: 포기 성공 여부
        """
        if quest_id in self.player_quests:
            del self.player_quests[quest_id]
            return True
        return False
    
    def update_kill_progress(self, monster_name: str) -> List[str]:
        """
        몬스터 처치 시 관련 퀘스트 진행도 업데이트
        
        Args:
            monster_name: 처치한 몬스터 이름
            
        Returns:
            List[str]: 완료된 퀘스트 ID 목록
        """
        completed_quests = []
        
        for quest_id, quest_data in self.player_quests.items():
            if quest_data["type"] == "kill" and quest_data["objectives"]["target"] == monster_name:
                quest_data["objectives"]["current"] += 1
                
                # 목표 달성 확인
                if quest_data["objectives"]["current"] >= quest_data["objectives"]["count"]:
                    quest_data["status"] = "completed"
                    completed_quests.append(quest_id)
        
        return completed_quests
    
    def update_collect_progress(self, item_name: str, amount: int = 1) -> List[str]:
        """
        아이템 수집 시 관련 퀘스트 진행도 업데이트
        
        Args:
            item_name: 수집한 아이템 이름
            amount: 수집한 개수
            
        Returns:
            List[str]: 완료된 퀘스트 ID 목록
        """
        completed_quests = []
        
        for quest_id, quest_data in self.player_quests.items():
            if quest_data["type"] == "collect" and quest_data["objectives"]["target"] == item_name:
                quest_data["objectives"]["current"] += amount
                
                # 목표 달성 확인 (초과 수집 방지)
                if quest_data["objectives"]["current"] >= quest_data["objectives"]["count"]:
                    quest_data["objectives"]["current"] = quest_data["objectives"]["count"]
                    quest_data["status"] = "completed"
                    completed_quests.append(quest_id)
        
        return completed_quests
    
    def update_travel_progress(self, region_name: str) -> List[str]:
        """
        지역 이동 시 관련 퀘스트 진행도 업데이트
        
        Args:
            region_name: 도착한 지역 이름
            
        Returns:
            List[str]: 완료된 퀘스트 ID 목록
        """
        completed_quests = []
        
        for quest_id, quest_data in self.player_quests.items():
            if quest_data["type"] == "travel" and quest_data["objectives"]["target"] == region_name:
                quest_data["objectives"]["current"] = 1
                quest_data["status"] = "completed"
                completed_quests.append(quest_id)
        
        return completed_quests
    
    def complete_quest(self, quest_id: str) -> Optional[Dict]:
        """
        퀘스트 완료 처리 및 보상 반환
        
        Args:
            quest_id: 완료할 퀘스트 ID
            
        Returns:
            Optional[Dict]: 보상 정보 (None이면 완료 실패)
        """
        if quest_id not in self.player_quests:
            return None
        
        quest_data = self.player_quests[quest_id]
        if quest_data["status"] != "completed":
            return None
        
        # 완료된 퀘스트를 완료 목록에 추가
        self.completed_quests.add(quest_id)
        
        # 진행 중 퀘스트에서 제거
        del self.player_quests[quest_id]
        
        # 보상 정보 반환
        return quest_data["rewards"]
    
    def get_active_quests(self) -> List[Dict]:
        """진행 중인 퀘스트 목록 반환"""
        return list(self.player_quests.values())
    
    def get_quest_progress_display(self, quest_id: str) -> str:
        """
        퀘스트 진행도를 시각적으로 표시
        
        Args:
            quest_id: 퀘스트 ID
            
        Returns:
            str: 진행도 표시 문자열
        """
        if quest_id not in self.player_quests:
            return "퀘스트를 찾을 수 없습니다."
        
        quest_data = self.player_quests[quest_id]
        current = quest_data["objectives"]["current"]
        target = quest_data["objectives"]["count"]
        
        # 진행률 계산
        progress = min(current, target)
        percentage = (progress / target) * 100
        
        # 진행률 바 생성
        bar_length = 15
        filled_length = int(bar_length * progress / target)
        bar = "■" * filled_length + "□" * (bar_length - filled_length)
        
        return f"[{bar}] {progress}/{target} ({percentage:.0f}%)"
    
    def display_available_quests(self, player_level: int, player_region: str):
        """수락 가능한 퀘스트 목록 표시"""
        available = self.get_available_quests(player_level, player_region)
        
        if not available:
            print(f"📋 {player_region}에서 수락 가능한 퀘스트가 없습니다.")
            return
        
        print(f"📋 === {player_region} 지역 퀘스트 === 📋")
        print()
        
        for i, quest in enumerate(available, 1):
            print(f"{i}. 🎯 {quest['title']}")
            print(f"   📖 {quest['description']}")
            
            # 목표 표시
            obj = quest['objectives']
            if quest['type'] == 'kill':
                print(f"   ⚔️ 목표: {obj['target']} {obj['count']}마리 처치")
            elif quest['type'] == 'collect':
                print(f"   📦 목표: {obj['target']} {obj['count']}개 수집")
            elif quest['type'] == 'travel':
                print(f"   🚶‍♂️ 목표: {obj['target']}에 도달")
            
            # 보상 표시
            rewards = quest['rewards']
            reward_text = f"경험치 {rewards['exp']}"
            if 'items' in rewards:
                items = [f"{name} {count}개" for name, count in rewards['items'].items()]
                reward_text += f", {', '.join(items)}"
            print(f"   🎁 보상: {reward_text}")
            
            # 조건 표시
            req = quest['requirements']
            if req['min_level'] > 1:
                print(f"   📊 필요 레벨: {req['min_level']}")
            if req['completed_quests']:
                print(f"   ✅ 선행 퀘스트: {', '.join(req['completed_quests'])}")
            
            print()
    
    def display_active_quests(self):
        """진행 중인 퀘스트 목록 표시"""
        active = self.get_active_quests()
        
        if not active:
            print("📝 진행 중인 퀘스트가 없습니다.")
            return
        
        print("📝 === 진행 중인 퀘스트 === 📝")
        print()
        
        for quest in active:
            status_icon = "✅" if quest['status'] == 'completed' else "⏳"
            print(f"{status_icon} {quest['title']} ({quest['region']})")
            print(f"   📖 {quest['description']}")
            
            # 진행도 표시
            progress_bar = self.get_quest_progress_display(quest['id'])
            obj = quest['objectives']
            
            if quest['type'] == 'kill':
                print(f"   ⚔️ 처치: {obj['target']} {progress_bar}")
            elif quest['type'] == 'collect':
                print(f"   📦 수집: {obj['target']} {progress_bar}")
            elif quest['type'] == 'travel':
                print(f"   🚶‍♂️ 이동: {obj['target']} {progress_bar}")
            
            print()
    
    def save_quest_progress(self, filename: str = "quest_save.json"):
        """퀘스트 진행상황 저장"""
        save_data = {
            "player_quests": self.player_quests,
            "completed_quests": list(self.completed_quests)
        }
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❗ 퀘스트 저장 실패: {e}")
            return False
    
    def load_quest_progress(self, filename: str = "quest_save.json"):
        """퀘스트 진행상황 로드"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                save_data = json.load(f)
            
            self.player_quests = save_data.get("player_quests", {})
            self.completed_quests = set(save_data.get("completed_quests", []))
            return True
        except FileNotFoundError:
            # 저장 파일이 없으면 초기 상태로 시작
            self.player_quests = {}
            self.completed_quests = set()
            return True
        except Exception as e:
            print(f"❗ 퀘스트 로드 실패: {e}")
            return False


# 전역 퀘스트 시스템 인스턴스
quest_system = QuestSystem()


def get_quest_system():
    """퀘스트 시스템 인스턴스 반환"""
    return quest_system


# 편의 함수들
def accept_quest(quest_id: str) -> bool:
    """퀘스트 수락"""
    return quest_system.accept_quest(quest_id)


def complete_quest(quest_id: str) -> Optional[Dict]:
    """퀘스트 완료"""
    return quest_system.complete_quest(quest_id)


def update_kill_quest(monster_name: str) -> List[str]:
    """몬스터 처치 퀘스트 업데이트"""
    return quest_system.update_kill_progress(monster_name)


def update_collect_quest(item_name: str, amount: int = 1) -> List[str]:
    """수집 퀘스트 업데이트"""
    return quest_system.update_collect_progress(item_name, amount)


def update_travel_quest(region_name: str) -> List[str]:
    """이동 퀘스트 업데이트"""
    return quest_system.update_travel_progress(region_name)


def show_available_quests(player_level: int, player_region: str):
    """수락 가능한 퀘스트 표시"""
    quest_system.display_available_quests(player_level, player_region)


def show_active_quests():
    """진행 중인 퀘스트 표시"""
    quest_system.display_active_quests() 