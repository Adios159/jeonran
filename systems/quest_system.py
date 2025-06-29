"""
전란 그리고 요괴 - 조선시대 RPG
파일: systems/quest_system.py
설명: 퀘스트 관리 시스템
"""

import json
import os
from typing import List, Dict, Optional, Any

__all__ = ["Quest", "QuestSystem"]

class Quest:
    """개별 퀘스트 클래스"""
    def __init__(self, quest_data: Dict[str, Any]):
        self.id: str = quest_data.get("id", "")
        self.title: str = quest_data.get("title", "알 수 없는 의뢰")
        self.giver: str = quest_data.get("giver", "익명")
        self.region: str = quest_data.get("region", "")
        self.description: str = quest_data.get("description", "...")
        self.condition: Dict[str, Any] = quest_data.get("condition", {})
        self.reward: Dict[str, Any] = quest_data.get("reward", {})
        self.tags: List[str] = quest_data.get("tags", [])

    def get_summary(self) -> str:
        """퀘스트 요약 정보 반환"""
        return f"📜 [{self.region}] {self.title} (의뢰인: {self.giver})"

    def get_details(self) -> str:
        """퀘스트 상세 정보 반환"""
        details = [
            f"📜 **{self.title}**",
            f"  - 의뢰인: {self.giver} ({self.region})",
            f"  - 설명: {self.description}",
            f"  - 조건: {self._get_condition_str()}",
            f"  - 보상: {self._get_reward_str()}",
            f"  - 태그: {', '.join(self.tags)}"
        ]
        return "\n".join(details)

    def _get_condition_str(self) -> str:
        """조건을 설명하는 문자열 반환"""
        cond_type = self.condition.get("type")
        if cond_type == "kill":
            return f"{self.condition.get('target_type', '요괴')} {self.condition.get('count', 0)}마리 처치"
        elif cond_type == "collect":
            return f"{self.condition.get('item_name', '')} {self.condition.get('count', 0)}개 수집"
        elif cond_type == "kill_with_status":
            return f"{self.condition.get('status')} 상태의 적 {self.condition.get('count', 0)}마리 처치"
        elif cond_type == "kill_list":
            return f"지정된 요괴 ({', '.join(self.condition.get('targets', []))}) 각각 처치"
        return "알 수 없는 조건"

    def _get_reward_str(self) -> str:
        """보상을 설명하는 문자열 반환"""
        parts = []
        if "exp" in self.reward:
            parts.append(f"경험치 {self.reward['exp']}")
        if "gold" in self.reward:
            parts.append(f"{self.reward['gold']}전")
        if "items" in self.reward:
            item_names = [f"{item['name']} x{item['count']}" for item in self.reward["items"]]
            parts.append(", ".join(item_names))
        return ", ".join(parts) if parts else "보상 없음"


class QuestSystem:
    """퀘스트 관리 시스템"""
    def __init__(self):
        self.quests: Dict[str, Quest] = {}
        self.quests_by_giver: Dict[str, List[Quest]] = {}
        self._load_quests()

    def _load_quests(self):
        """quests.json에서 퀘스트 데이터를 로드합니다."""
        quest_file = os.path.join("data", "quests.json")
        if not os.path.exists(quest_file):
            print("⚠️ quests.json 파일이 없습니다.")
            return
        
        try:
            with open(quest_file, 'r', encoding='utf-8') as file:
                quest_data_list = json.load(file)
            
            for quest_data in quest_data_list:
                quest = Quest(quest_data)
                self.quests[quest.id] = quest
                
                if quest.giver not in self.quests_by_giver:
                    self.quests_by_giver[quest.giver] = []
                self.quests_by_giver[quest.giver].append(quest)
                
            print(f"✅ {len(self.quests)}개의 퀘스트를 로드했습니다.")
        except Exception as e:
            print(f"❌ 퀘스트 데이터 로드 실패: {e}")

    def get_quest(self, quest_id: str) -> Optional[Quest]:
        """퀘스트 ID로 퀘스트를 조회합니다."""
        return self.quests.get(quest_id)

    def get_quests_for_giver(self, giver_name: str) -> List[Quest]:
        """특정 NPC가 제공하는 퀘스트 목록을 반환합니다."""
        return self.quests_by_giver.get(giver_name, [])

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