"""
전란 그리고 요괴 - 조선시대 RPG
파일: systems/weapon_system.py
설명: 무기 시스템 및 장착 관리
"""

import json
import os
from typing import List, Dict, Optional


class Weapon:
    """무기 클래스"""
    
    def __init__(self, weapon_data: Dict):
        self.id: str = weapon_data.get("id", "")
        self.name: str = weapon_data.get("name", "알 수 없는 무기")
        self.type: str = weapon_data.get("type", "기타")
        self.attack: int = weapon_data.get("attack", 0)
        self.rarity: str = weapon_data.get("rarity", "일반")
        self.description: str = weapon_data.get("description", "")
        self.price: int = weapon_data.get("price", 0)
        self.usable_classes: List[str] = weapon_data.get("usable_classes", [])
        self.special_effect: str = weapon_data.get("special_effect", "")
    
    def get_effective_attack(self, player_class: str) -> int:
        """플레이어 직업에 따른 효과적인 공격력을 계산합니다."""
        if player_class == "유랑객":
            if self.type == "한손검":
                return int(self.attack * 0.85)
            elif self.type == "두손검":
                return int(self.attack * 0.65)
            elif self.type in ["부적", "비파"]:
                raise ValueError(f"{player_class}은(는) {self.type}을(를) 사용할 수 없습니다.")
        
        return self.attack
    
    def can_be_used_by(self, player_class: str) -> bool:
        """해당 직업이 이 무기를 사용할 수 있는지 확인합니다."""
        if player_class == "유랑객" and self.type in ["부적", "비파"]:
            return False
        return player_class in self.usable_classes
    
    def get_rarity_color(self) -> str:
        """희귀도에 따른 색상 이모지를 반환합니다."""
        colors = {
            "일반": "⚪",
            "희귀": "🟣", 
            "전설": "🟡"
        }
        return colors.get(self.rarity, "⚪")
    
    def get_info(self, player_class: str = None) -> str:
        """무기 정보를 상세히 반환합니다."""
        info = f"{self.get_rarity_color()} **{self.name}** ({self.type})\n"
        
        # 공격력 표시 (직업별 보정 적용)
        if player_class:
            try:
                effective_attack = self.get_effective_attack(player_class)
                if effective_attack != self.attack:
                    info += f"   ⚔️ 공격력: {self.attack} → {effective_attack} ({player_class} 보정)\n"
                else:
                    info += f"   ⚔️ 공격력: {self.attack}\n"
            except ValueError as e:
                info += f"   ❌ {str(e)}\n"
        else:
            info += f"   ⚔️ 공격력: {self.attack}\n"
        
        info += f"   💰 가격: {self.price}전\n"
        info += f"   📝 {self.description}\n"
        
        if self.special_effect:
            info += f"   ✨ 특수 효과: {self.special_effect}\n"
        
        # 사용 가능 직업
        info += f"   👥 사용 가능: {', '.join(self.usable_classes)}"
        
        return info


class WeaponSystem:
    """무기 관리 시스템"""
    
    def __init__(self):
        self.weapons: Dict[str, Weapon] = {}
        self.weapons_by_type: Dict[str, List[Weapon]] = {}
        self.load_weapons()
    
    def load_weapons(self):
        """weapons.json에서 무기 데이터를 로드합니다."""
        weapon_file = os.path.join("data", "weapons.json")
        
        if not os.path.exists(weapon_file):
            print("⚠️ weapons.json 파일이 없습니다.")
            return
        
        try:
            with open(weapon_file, 'r', encoding='utf-8') as file:
                weapon_data_list = json.load(file)
            
            # 무기 객체 생성 및 저장
            for weapon_data in weapon_data_list:
                weapon = Weapon(weapon_data)
                self.weapons[weapon.id] = weapon
                
                # 타입별 무기 분류
                if weapon.type not in self.weapons_by_type:
                    self.weapons_by_type[weapon.type] = []
                self.weapons_by_type[weapon.type].append(weapon)
            
            print(f"✅ {len(self.weapons)}개의 무기를 로드했습니다.")
            
        except Exception as e:
            print(f"❌ 무기 데이터 로드 실패: {e}")
    
    def get_weapon(self, weapon_id: str) -> Optional[Weapon]:
        """무기 ID로 무기를 조회합니다."""
        return self.weapons.get(weapon_id)
    
    def get_weapon_by_name(self, name: str) -> Optional[Weapon]:
        """무기 이름으로 무기를 조회합니다."""
        for weapon in self.weapons.values():
            if weapon.name == name:
                return weapon
        return None
    
    def get_weapons_by_type(self, weapon_type: str) -> List[Weapon]:
        """특정 타입의 무기 목록을 반환합니다."""
        return self.weapons_by_type.get(weapon_type, [])
    
    def get_usable_weapons(self, player_class: str) -> List[Weapon]:
        """특정 직업이 사용할 수 있는 무기 목록을 반환합니다."""
        usable_weapons = []
        for weapon in self.weapons.values():
            if weapon.can_be_used_by(player_class):
                usable_weapons.append(weapon)
        return usable_weapons
    
    def get_weapons_by_rarity(self, rarity: str) -> List[Weapon]:
        """특정 희귀도의 무기 목록을 반환합니다."""
        return [weapon for weapon in self.weapons.values() if weapon.rarity == rarity]
    
    def get_weapons_in_price_range(self, min_price: int, max_price: int) -> List[Weapon]:
        """가격 범위 내의 무기 목록을 반환합니다."""
        return [weapon for weapon in self.weapons.values() 
                if min_price <= weapon.price <= max_price]
    
    def search_weapons(self, keyword: str) -> List[Weapon]:
        """키워드로 무기를 검색합니다."""
        results = []
        keyword_lower = keyword.lower()
        
        for weapon in self.weapons.values():
            if (keyword_lower in weapon.name.lower() or 
                keyword_lower in weapon.description.lower() or
                keyword_lower in weapon.type.lower()):
                results.append(weapon)
        
        return results
    
    def show_weapon_catalog(self, player_class: str = None):
        """무기 도감을 표시합니다."""
        print("\n⚔️ **무기 도감**")
        print("=" * 50)
        
        # 타입별로 분류하여 표시
        for weapon_type, weapons in self.weapons_by_type.items():
            print(f"\n📂 **{weapon_type}**")
            print("-" * 30)
            
            for weapon in sorted(weapons, key=lambda w: w.price):
                # 직업 제한 확인
                if player_class and not weapon.can_be_used_by(player_class):
                    continue
                
                print(f"  {weapon.get_rarity_color()} {weapon.name}")
                print(f"    공격력: {weapon.attack} | 가격: {weapon.price}전")
                
                if player_class:
                    try:
                        effective_attack = weapon.get_effective_attack(player_class)
                        if effective_attack != weapon.attack:
                            print(f"    → {player_class} 효과적 공격력: {effective_attack}")
                    except ValueError:
                        print(f"    ❌ {player_class}은(는) 사용 불가")
                
                print()
    
    def show_weapons_by_class(self, player_class: str):
        """특정 직업이 사용할 수 있는 무기들을 표시합니다."""
        usable_weapons = self.get_usable_weapons(player_class)
        
        if not usable_weapons:
            print(f"❌ {player_class}이(가) 사용할 수 있는 무기가 없습니다.")
            return
        
        print(f"\n⚔️ **{player_class} 전용 무기**")
        print("=" * 40)
        
        # 타입별로 그룹화
        weapons_by_type = {}
        for weapon in usable_weapons:
            if weapon.type not in weapons_by_type:
                weapons_by_type[weapon.type] = []
            weapons_by_type[weapon.type].append(weapon)
        
        for weapon_type, weapons in weapons_by_type.items():
            print(f"\n📂 **{weapon_type}**")
            print("-" * 20)
            
            for weapon in sorted(weapons, key=lambda w: w.price):
                effective_attack = weapon.get_effective_attack(player_class)
                penalty_info = ""
                if effective_attack != weapon.attack:
                    penalty_info = f" → {effective_attack}"
                
                print(f"  {weapon.get_rarity_color()} {weapon.name}")
                print(f"    공격력: {weapon.attack}{penalty_info} | 가격: {weapon.price}전")
                if weapon.special_effect:
                    print(f"    ✨ {weapon.special_effect}")
                print()


def test_weapon_system():
    """무기 시스템 테스트 함수"""
    print("🧪 무기 시스템 테스트 시작")
    print("=" * 40)
    
    # 무기 시스템 초기화
    weapon_system = WeaponSystem()
    
    # 1. 전체 무기 카탈로그
    weapon_system.show_weapon_catalog()
    
    # 2. 유랑객 전용 무기 표시
    print("\n" + "="*40)
    print("🥷 유랑객 무기 테스트")
    weapon_system.show_weapons_by_class("유랑객")
    
    # 3. 무사 전용 무기 표시
    print("\n" + "="*40)
    print("⚔️ 무사 무기 테스트")
    weapon_system.show_weapons_by_class("무사")
    
    # 4. 도사 전용 무기 표시
    print("\n" + "="*40)
    print("🔮 도사 무기 테스트")
    weapon_system.show_weapons_by_class("도사")
    
    # 5. 성능 보정 테스트
    print("\n" + "="*40)
    print("📊 성능 보정 테스트")
    
    # 한손검 테스트
    sword = weapon_system.get_weapon_by_name("조선도")
    if sword:
        print(f"조선도 기본 공격력: {sword.attack}")
        print(f"무사 사용 시: {sword.get_effective_attack('무사')}")
        print(f"유랑객 사용 시: {sword.get_effective_attack('유랑객')} (85% 보정)")
    
    # 두손검 테스트
    hidden_blade = weapon_system.get_weapon_by_name("두손검")
    if hidden_blade:
        print(f"\n두손검 기본 공격력: {hidden_blade.attack}")
        print(f"유랑객 사용 시: {hidden_blade.get_effective_attack('유랑객')} (65% 보정)")
    
    # 부적 테스트 (유랑객 사용 불가)
    talisman = weapon_system.get_weapon_by_name("화염 부적")
    if talisman:
        print(f"\n화염 부적:")
        try:
            talisman.get_effective_attack("유랑객")
        except ValueError as e:
            print(f"  유랑객: {e}")
        print(f"  도사 사용 시: {talisman.get_effective_attack('도사')}")
    
    print("\n✅ 무기 시스템 테스트 완료!")


if __name__ == "__main__":
    test_weapon_system() 