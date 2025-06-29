from characters.base_character import BaseCharacter
from skills.warrior_skills import warrior_skills
from skills.mage_skills import mage_skills
from skills.rogue_skills import rogue_skills
from systems.inventory import Inventory
from systems.item import basic_items
from systems.weapon_system import WeaponSystem, Weapon
from systems.quest_system import Quest, quest_system
from typing import Optional, Dict, List, Any

class Player(BaseCharacter):
    # --- Static attribute declarations for type checkers ---
    level: int
    exp: int
    mp: int
    max_mp: int
    current_location: str
    gold: int
    inventory: 'Inventory'
    weapon_system: 'WeaponSystem'
    equipped_weapon: Optional['Weapon']
    active_quests: Dict[str, Dict[str, Any]]
    completed_quests: List[str]

    def __init__(self, name, job):
        self.job = job

        if job == "무사":
            max_hp = 120
            attack = 18
            defence = 15
            speed = 8
            skills = ["가르기"]
            max_mp = 20

        elif job == "도사":
            max_hp = 80
            attack = 12
            defence = 8
            speed = 10
            skills = ["화염부"]
            max_mp = 40

        elif job == "유랑객":
            max_hp = 90
            attack = 14
            defence = 10
            speed = 18
            skills = ["급소찌르기"]
            max_mp = 30

        else:
            raise ValueError("없는 직업 입니다.")
        
        super().__init__(name, max_hp, attack, defence, speed)

        self.level = 1
        self.exp = 0
        self.mp = max_mp  # 초기 MP는 최대 MP로 설정
        self.max_mp = max_mp  # 최대 MP 속성 추가
        self.current_location = "한양"  # 기본 시작 위치
        self.gold = 0  # 초기 소지금

        # 직업별 스킬 할당
        if job == "무사":
            self.skills = warrior_skills
        elif job == "도사":
            self.skills = mage_skills
        elif job == "유랑객":
            self.skills = rogue_skills
        else:
            raise ValueError("없는 직업 입니다")
        
        # 인벤토리 초기화
        self.inventory = Inventory()
        
        # 무기 시스템 초기화
        self.weapon_system = WeaponSystem()
        self.equipped_weapon = None  # 현재 장착한 무기
        self.base_attack = attack    # 기본 공격력 저장 (무기 없을 때)

        # 퀘스트 관련 초기화
        self.active_quests = {}
        self.completed_quests = []
    
    # 속성 별칭 제공 (type checker용)
    @property
    def hp(self):
        return self.current_hp

    @hp.setter
    def hp(self, value):
        self.current_hp = value

    @property
    def defense(self):
        return self.defence

    @property
    def location(self):
        return self.current_location
    
    @location.setter
    def location(self, value):
        self.current_location = value

    def get_effective_attack(self) -> int:
        """현재 장비와 보정을 반영한 실제 공격력 반환"""
        return self.attack

    def show_exp_progress(self):
        """경험치 진행 상황을 간단히 출력합니다."""
        progress = int((self.exp / (self.level * 100)) * 20)
        bar = "■" * progress + "□" * (20 - progress)
        pct = (self.exp / (self.level * 100)) * 100
        print(f"EXP [{bar}] {pct:.1f}%")
    
    def give_starting_items(self):
        """시작 아이템 지급"""
        print("\n=== 시작 아이템 지급 ===")
        self.inventory.add_item("소형 약초", 3)
        self.inventory.add_item("마력 물약", 2)
    
    def end_turn(self):
        # 부모 클래스의 상태이상 처리
        super().end_turn()
        
        # 레벨에 따른 최대 MP 업데이트
        self.max_mp = 30 + 5 * (self.level - 1)
        old_mp = self.mp
        self.mp = min(self.mp + 2, self.max_mp)
        if self.mp > old_mp:
            print(f"{self.name}의 마력이 {self.mp - old_mp}만큼 회복되었다 (MP: {self.mp}/{self.max_mp})")
    
    def gain_exp(self, amount):
        """경험치 획득 및 레벨업 처리"""
        # 지역별 경험치 보너스 적용 (향후 구현)
        self.exp += amount
        print(f"경험치 {amount} 획득! (총 경험치: {self.exp})")
        
        # 레벨업 체크 (경험치 100마다 레벨업)
        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level += 1
            
            # 레벨업 보상
            hp_increase = 10
            attack_increase = 2
            defence_increase = 1
            mp_increase = 5
            
            self.max_hp += hp_increase
            self.current_hp += hp_increase  # 레벨업 시 HP도 회복
            self.attack += attack_increase
            self.defence += defence_increase
            
            print(f"\n🎉 레벨업! {self.level-1} → {self.level}")
            print(f"HP +{hp_increase} (최대 HP: {self.max_hp})")
            print(f"공격력 +{attack_increase} (현재: {self.attack})")
            print(f"방어력 +{defence_increase} (현재: {self.defence})")
            print(f"최대 MP +{mp_increase} (현재: 30 + {mp_increase * (self.level-1)})")
            
            # MP 최대치도 증가
            self.max_mp = 30 + mp_increase * (self.level - 1)
            self.mp = min(self.mp + mp_increase, self.max_mp)
    
    def use_item(self, item_name):
        """아이템 사용"""
        if not self.inventory.has_item(item_name):
            print(f"{item_name}이(가) 인벤토리에 없습니다.")
            return False
        
        if item_name not in basic_items:
            print(f"{item_name}은(는) 사용할 수 없는 아이템입니다.")
            return False
        
        item = basic_items[item_name]
        if item.use(self):  # 아이템 사용 성공
            self.inventory.remove_item(item_name, 1)
            return True
        return False
    
    def equip_weapon(self, weapon: Weapon) -> bool:
        """무기를 장착합니다."""
        # 직업 제한 확인
        if not weapon.can_be_used_by(self.job):
            print(f"❌ {self.job}은(는) {weapon.name}을(를) 사용할 수 없습니다.")
            return False
        
        # 기존 무기 해제
        if self.equipped_weapon:
            print(f"🔄 {self.equipped_weapon.name}을(를) 해제하고 {weapon.name}을(를) 장착합니다.")
        else:
            print(f"⚔️ {weapon.name}을(를) 장착했습니다!")
        
        self.equipped_weapon = weapon
        self._update_attack()
        return True
    
    def unequip_weapon(self):
        """무기를 해제합니다."""
        if not self.equipped_weapon:
            print("❌ 장착된 무기가 없습니다.")
            return False
        
        print(f"🔄 {self.equipped_weapon.name}을(를) 해제했습니다.")
        self.equipped_weapon = None
        self._update_attack()
        return True
    
    def _update_attack(self):
        """무기에 따른 공격력을 업데이트합니다."""
        if self.equipped_weapon:
            try:
                weapon_attack = self.equipped_weapon.get_effective_attack(self.job)
                self.attack = self.base_attack + weapon_attack
            except ValueError as e:
                print(f"⚠️ 무기 장착 오류: {e}")
                self.attack = self.base_attack
        else:
            self.attack = self.base_attack
    
    def get_weapon_info(self) -> str:
        """현재 장착된 무기 정보를 반환합니다."""
        if not self.equipped_weapon:
            return "❌ 장착된 무기가 없습니다."
        
        weapon = self.equipped_weapon
        try:
            effective_attack = weapon.get_effective_attack(self.job)
            info = f"⚔️ **장착 중**: {weapon.name}\n"
            info += f"   🏷️ 타입: {weapon.type}\n"
            info += f"   ⚡ 기본 공격력: {weapon.attack}\n"
            
            if effective_attack != weapon.attack:
                info += f"   📊 효과적 공격력: {effective_attack} ({self.job} 보정)\n"
            
            if weapon.special_effect:
                info += f"   ✨ 특수 효과: {weapon.special_effect}\n"
            
            info += f"   💰 가치: {weapon.price}전"
            return info
            
        except ValueError as e:
            return f"❌ 무기 오류: {e}"
    
    def show_equipment_status(self):
        """장비 상태를 표시합니다."""
        print("\n⚔️ **장비 상태**")
        print("=" * 30)
        print(f"🧑 캐릭터: {self.name} ({self.job})")
        print(f"💪 기본 공격력: {self.base_attack}")
        print(f"⚔️ 현재 총 공격력: {self.attack}")
        print()
        print(self.get_weapon_info())
    
    def search_weapons(self, keyword: Optional[str] = None):
        """무기를 검색하고 표시합니다."""
        if keyword:
            weapons = self.weapon_system.search_weapons(keyword)
            print(f"\n🔍 '{keyword}' 검색 결과:")
        else:
            weapons = self.weapon_system.get_usable_weapons(self.job)
            print(f"\n⚔️ {self.job} 사용 가능한 무기:")
        
        if not weapons:
            print("❌ 해당하는 무기가 없습니다.")
            return
        
        print("=" * 40)
        for i, weapon in enumerate(weapons, 1):
            print(f"{i}. {weapon.get_info(self.job)}")
            print("-" * 30)
    
    def buy_weapon(self, weapon_id: str, price: int) -> bool:
        """무기를 구매합니다 (상점 시스템에서 호출)."""
        weapon = self.weapon_system.get_weapon(weapon_id)
        if not weapon:
            print(f"❌ 무기를 찾을 수 없습니다: {weapon_id}")
            return False
        
        # 직업 제한 확인
        if not weapon.can_be_used_by(self.job):
            print(f"❌ {self.job}은(는) {weapon.name}을(를) 사용할 수 없습니다.")
            return False
        
        # 인벤토리에 무기 추가 (향후 구현)
        print(f"✅ {weapon.name}을(를) 구매했습니다!")
        return True

    def accept_quest(self, quest_id: str) -> bool:
        """퀘스트를 수락합니다."""
        if quest_id in self.active_quests or quest_id in self.completed_quests:
            print("이미 수락했거나 완료한 퀘스트입니다.")
            return False
        
        quest = quest_system.get_quest(quest_id)
        if not quest:
            print("존재하지 않는 퀘스트입니다.")
            return False
            
        self.active_quests[quest_id] = {"progress": {}} # 진행상황 초기화
        print(f"\n[퀘스트 수락] {quest.title}")
        print(quest.get_details())
        return True

    def show_quest_log(self):
        """퀘스트 로그를 표시합니다."""
        print("\n" + "="*50)
        print("📖 퀘스트 로그")
        print("="*50)

        if not self.active_quests:
            print("\n진행 중인 퀘스트가 없습니다.")
        else:
            print("\n--- 진행 중인 퀘스트 ---")
            for quest_id in self.active_quests:
                quest = quest_system.get_quest(quest_id)
                if quest:
                    print(f"\n{quest.get_summary()}")
                    # 여기에 상세 진행상황을 표시할 수 있습니다.
        
        if not self.completed_quests:
            print("\n완료한 퀘스트가 없습니다.")
        else:
            print("\n--- 완료한 퀘스트 ---")
            for quest_id in self.completed_quests:
                quest = quest_system.get_quest(quest_id)
                if quest:
                    print(f"  - {quest.title} (완료)")
        
        print("\n" + "="*50)