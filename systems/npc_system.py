"""
전란 그리고 요괴 - 조선시대 RPG
파일: systems/npc_system.py
설명: NPC 관리 및 상호작용 시스템
"""

__all__ = [
    "NPCSystem",
    "handle_npc_interaction",
]

import json
import os
from typing import List, Dict, Optional
from systems.quest_system import quest_system


class NPC:
    """개별 NPC 클래스"""
    
    def __init__(self, npc_data: Dict):
        self.id: str = npc_data.get("id", "")
        self.name: str = npc_data.get("name", "알 수 없는 인물")
        self.region: str = npc_data.get("region", "")
        self.dialogue: str = npc_data.get("dialogue", "...")
        self.type: str = npc_data.get("type", "일반")
        self.shop_id: Optional[str] = npc_data.get("shop_id")
        self.has_quest = "quest_giver" in npc_data.get("tags", [])
        
    def speak(self) -> str:
        """NPC의 대사를 반환합니다."""
        return f'💬 "{self.dialogue}"'
    
    def get_info(self) -> str:
        """NPC의 기본 정보를 반환합니다."""
        info = f"🧑 **{self.name}** ({self.region})"
        if self.type == "상점":
            info += " 🏪"
        return info
    
    def has_shop(self) -> bool:
        """상점을 운영하는 NPC인지 확인합니다."""
        return self.shop_id is not None and self.type == "상점"


class NPCSystem:
    """NPC 관리 시스템"""
    
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self.npcs_by_region: Dict[str, List[NPC]] = {}
        self.load_npcs()
    
    def load_npcs(self):
        """npcs.json에서 NPC 데이터를 로드합니다."""
        npc_file = os.path.join("data", "npcs.json")
        
        if not os.path.exists(npc_file):
            print("⚠️ npcs.json 파일이 없습니다.")
            return
        
        try:
            with open(npc_file, 'r', encoding='utf-8') as file:
                npc_data_list = json.load(file)
                
            # NPC 객체 생성 및 저장
            for npc_data in npc_data_list:
                npc = NPC(npc_data)
                self.npcs[npc.id] = npc
                
                # 지역별 NPC 분류
                if npc.region not in self.npcs_by_region:
                    self.npcs_by_region[npc.region] = []
                self.npcs_by_region[npc.region].append(npc)
                
            print(f"✅ {len(self.npcs)}명의 NPC를 로드했습니다.")
            
        except Exception as e:
            print(f"❌ NPC 데이터 로드 실패: {e}")
    
    def get_npcs_in_region(self, region_name: str) -> List[NPC]:
        """특정 지역의 NPC 목록을 반환합니다."""
        return self.npcs_by_region.get(region_name, [])
    
    def get_npc(self, npc_id: str) -> Optional[NPC]:
        """특정 NPC를 ID로 조회합니다."""
        return self.npcs.get(npc_id)
    
    def get_npc_by_name(self, name: str, region: Optional[str] = None) -> Optional[NPC]:
        """이름으로 NPC를 조회합니다. 지역을 지정하면 해당 지역에서만 검색합니다."""
        search_npcs = []
        
        if region:
            search_npcs = self.get_npcs_in_region(region)
        else:
            search_npcs = list(self.npcs.values())
        
        for npc in search_npcs:
            if npc.name == name:
                return npc
        return None
    
    def show_region_npcs(self, region_name: str) -> bool:
        """특정 지역의 NPC 목록을 표시합니다."""
        npcs = self.get_npcs_in_region(region_name)
        
        if not npcs:
            print(f"📭 {region_name}에는 만날 수 있는 사람이 없습니다.")
            return False
        
        print(f"\n🏘️ **{region_name}의 사람들**")
        print("=" * 40)
        
        for i, npc in enumerate(npcs, 1):
            quest_marker = " ❔" if npc.has_quest else ""
            print(f"{i}. {npc.name}{quest_marker}")
        
        print("=" * 40)
        return True
    
    def interact_with_npc(self, npc: NPC) -> str:
        """NPC와 상호작용합니다."""
        result = f"\n{npc.get_info()}\n"
        result += f"{npc.speak()}\n"
        
        if npc.has_shop():
            result += "\n🏪 [상점 이용 가능] (상점 시스템 구현 예정)"
        
        return result
    
    def select_npc_in_region(self, region_name: str) -> Optional[NPC]:
        """지역에서 NPC를 선택하는 인터페이스입니다."""
        npcs = self.get_npcs_in_region(region_name)
        
        if not npcs:
            return None
        
        if not self.show_region_npcs(region_name):
            return None
        
        while True:
            try:
                print(f"\n만나고 싶은 사람을 선택하세요 (1-{len(npcs)}, 0: 취소): ", end="")
                choice = input().strip()
                
                if choice == "0":
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(npcs):
                    return npcs[choice_num - 1]
                else:
                    print(f"⚠️ 1부터 {len(npcs)} 사이의 숫자를 입력하세요.")
                    
            except ValueError:
                print("⚠️ 올바른 숫자를 입력하세요.")
            except KeyboardInterrupt:
                print("\n👋 대화를 중단합니다.")
                return None
    
    def get_shop_npcs(self) -> List[NPC]:
        """상점을 운영하는 NPC 목록을 반환합니다."""
        return [npc for npc in self.npcs.values() if npc.has_shop()]
    
    def get_npc_count_by_region(self) -> Dict[str, int]:
        """지역별 NPC 수를 반환합니다."""
        return {region: len(npcs) for region, npcs in self.npcs_by_region.items()}
    
    def search_npcs(self, keyword: str) -> List[NPC]:
        """키워드로 NPC를 검색합니다 (이름 또는 대사에서)."""
        results = []
        keyword_lower = keyword.lower()
        
        for npc in self.npcs.values():
            if (keyword_lower in npc.name.lower() or 
                keyword_lower in npc.dialogue.lower()):
                results.append(npc)
        
        return results
    
    def show_all_npcs(self):
        """모든 NPC 정보를 지역별로 표시합니다."""
        print("\n🌍 **모든 지역의 NPC 현황**")
        print("=" * 50)
        
        total_npcs = 0
        shop_npcs = 0
        
        for region, npcs in self.npcs_by_region.items():
            print(f"\n📍 **{region}** ({len(npcs)}명)")
            print("-" * 30)
            
            for npc in npcs:
                shop_indicator = " 🏪" if npc.has_shop() else ""
                print(f"  • {npc.name}{shop_indicator}")
                if npc.has_shop():
                    shop_npcs += 1
            
            total_npcs += len(npcs)
        
        print("\n" + "=" * 50)
        print(f"📊 **총 {total_npcs}명** (상점 운영자: {shop_npcs}명)")


def test_npc_system():
    """NPC 시스템 테스트 함수"""
    print("🧪 NPC 시스템 테스트 시작")
    print("=" * 40)
    
    # NPC 시스템 초기화
    npc_system = NPCSystem()
    
    # 1. 전체 NPC 현황
    npc_system.show_all_npcs()
    
    # 2. 특정 지역 NPC 조회
    print("\n" + "="*40)
    print("🏰 한양 지역 NPC 조회")
    npc_system.show_region_npcs("한양")
    
    # 3. NPC와 상호작용 테스트
    print("\n" + "="*40)
    print("💬 NPC 상호작용 테스트")
    
    npc = npc_system.get_npc_by_name("늙은 도사", "한양")
    if npc:
        print(npc_system.interact_with_npc(npc))
    
    # 4. 상점 NPC 목록
    print("\n" + "="*40)
    print("🏪 상점 운영 NPC 목록")
    shop_npcs = npc_system.get_shop_npcs()
    for npc in shop_npcs:
        print(f"  • {npc.name} ({npc.region}) - {npc.shop_id}")
    
    # 5. NPC 검색 테스트
    print("\n" + "="*40)
    print("🔍 '약초' 키워드 검색")
    search_results = npc_system.search_npcs("약초")
    for npc in search_results:
        print(f"  • {npc.name} ({npc.region}): {npc.dialogue}")
    
    print("\n✅ NPC 시스템 테스트 완료!")


def handle_npc_interaction(player):
    """현재 지역의 NPC와 상호작용하는 간단한 래퍼 함수."""
    from systems.region import region_manager
    npc_system = NPCSystem()
    
    # NPC 선택 UI 개선
    npcs_in_region = npc_system.get_npcs_in_region(region_manager.current_region)
    if not npcs_in_region:
        print(f"📭 {region_manager.current_region}에는 만날 수 있는 사람이 없습니다.")
        return False

    print(f"\n🏘️ **{region_manager.current_region}의 사람들**")
    for i, npc in enumerate(npcs_in_region, 1):
        quest_marker = " ❔" if npc.has_quest else ""
        print(f"{i}. {npc.name}{quest_marker}")
    print("0. 돌아가기")

    try:
        choice = int(input("\n선택> "))
        if choice == 0:
            return False
        selected_npc = npcs_in_region[choice - 1]
    except (ValueError, IndexError):
        print("올바른 번호를 입력해주세요.")
        return False

    # NPC와 상호작용
    print(npc_system.interact_with_npc(selected_npc))

    # 퀘스트 처리
    available_quests = [
        q for q in quest_system.get_quests_for_giver(selected_npc.name)
        if q.id not in player.active_quests and q.id not in player.completed_quests
    ]

    if available_quests:
        print("\n--- 의뢰 가능 목록 ---")
        for i, quest in enumerate(available_quests, 1):
            print(f"{i}. {quest.title}")
        print("0. 거절하기")

        try:
            quest_choice = int(input("\n수락할 의뢰를 선택하세요: "))
            if quest_choice > 0:
                selected_quest = available_quests[quest_choice - 1]
                player.accept_quest(selected_quest.id)
        except (ValueError, IndexError):
            pass # 잘못된 입력은 무시

    input("\n계속하려면 엔터를 누르세요...")
    return True


if __name__ == "__main__":
    test_npc_system() 