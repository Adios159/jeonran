"""
전란 그리고 요괴 - 조선시대 RPG
파일: systems/shop_system.py
설명: 상점 시스템 및 거래 관리
"""

import json
import os
from typing import Dict, List, Optional
from systems.weapon_system import WeaponSystem
from systems.item import basic_items


class Shop:
    """상점 클래스"""
    
    def __init__(self, shop_data: Dict):
        self.id: str = shop_data.get("id", "")
        self.name: str = shop_data.get("name", "알 수 없는 상점")
        self.npc_name: str = shop_data.get("npc_name", "")
        self.region: str = shop_data.get("region", "")
        self.items: Dict[str, int] = shop_data.get("items", {})  # 아이템명: 재고
        self.weapons: List[str] = shop_data.get("weapons", [])   # 무기 ID 목록
        
        # 무기 시스템 참조
        self.weapon_system = WeaponSystem()
    
    def get_item_price(self, item_name: str) -> int:
        """아이템 가격을 반환합니다."""
        if item_name in basic_items:
            return basic_items[item_name].price
        return 0
    
    def has_item_in_stock(self, item_name: str) -> bool:
        """아이템 재고가 있는지 확인합니다."""
        return self.items.get(item_name, 0) > 0
    
    def has_weapon_in_stock(self, weapon_id: str) -> bool:
        """무기 재고가 있는지 확인합니다."""
        return weapon_id in self.weapons
    
    def show_shop_info(self):
        """상점 정보를 표시합니다."""
        print(f"\n🏪 **{self.name}**")
        print(f"📍 위치: {self.region}")
        print(f"👤 상인: {self.npc_name}")
        print("=" * 40)
    
    def show_items(self):
        """판매 중인 아이템을 표시합니다."""
        if not self.items:
            print("📦 판매 중인 소비 아이템이 없습니다.")
            return
        
        print("\n📦 **소비 아이템**")
        print("-" * 30)
        
        for item_name, stock in self.items.items():
            if item_name in basic_items:
                item = basic_items[item_name]
                stock_text = f"재고: {stock}개" if stock > 0 else "품절"
                print(f"💊 {item_name}")
                print(f"   💰 가격: {item.price}전")
                print(f"   📦 {stock_text}")
                print(f"   📝 {item.description}")
                print()
    
    def show_weapons(self, player_class: str = None):
        """판매 중인 무기를 표시합니다."""
        if not self.weapons:
            print("⚔️ 판매 중인 무기가 없습니다.")
            return
        
        print("\n⚔️ **무기**")
        print("-" * 30)
        
        for weapon_id in self.weapons:
            weapon = self.weapon_system.get_weapon(weapon_id)
            if weapon:
                # 직업 제한 확인
                usable = weapon.can_be_used_by(player_class) if player_class else True
                restriction_text = "" if usable else " ❌ 사용 불가"
                
                print(f"{weapon.get_rarity_color()} {weapon.name}{restriction_text}")
                print(f"   🏷️ 타입: {weapon.type}")
                print(f"   ⚔️ 공격력: {weapon.attack}")
                
                # 직업별 효과적 공격력 표시
                if player_class and usable:
                    try:
                        effective_attack = weapon.get_effective_attack(player_class)
                        if effective_attack != weapon.attack:
                            print(f"   📊 {player_class} 효과적 공격력: {effective_attack}")
                    except ValueError:
                        pass
                
                print(f"   💰 가격: {weapon.price}전")
                print(f"   📝 {weapon.description}")
                
                if weapon.special_effect:
                    print(f"   ✨ 특수 효과: {weapon.special_effect}")
                
                print()
    
    def buy_item(self, player, item_name: str) -> bool:
        """아이템을 구매합니다."""
        # 재고 확인
        if not self.has_item_in_stock(item_name):
            print(f"❌ {item_name}의 재고가 없습니다.")
            return False
        
        # 아이템 존재 확인
        if item_name not in basic_items:
            print(f"❌ {item_name}은(는) 판매하지 않는 아이템입니다.")
            return False
        
        price = self.get_item_price(item_name)
        
        # 금액 확인 (향후 Player에 money 필드 추가 시 활성화)
        # if player.money < price:
        #     print(f"❌ 금액이 부족합니다. 필요: {price}전, 보유: {player.money}전")
        #     return False
        
        # 인벤토리 용량 확인
        if not player.inventory.can_add_item():
            print("❌ 인벤토리가 가득 차서 아이템을 구매할 수 없습니다.")
            return False
        
        # 구매 처리
        player.inventory.add_item(item_name, 1)
        self.items[item_name] -= 1
        
        # 금액 차감 (향후 구현)
        # player.money -= price
        
        print(f"✅ {item_name}을(를) {price}전에 구매했습니다!")
        return True
    
    def buy_weapon(self, player, weapon_id: str) -> bool:
        """무기를 구매합니다."""
        # 재고 확인
        if not self.has_weapon_in_stock(weapon_id):
            print(f"❌ 해당 무기의 재고가 없습니다.")
            return False
        
        weapon = self.weapon_system.get_weapon(weapon_id)
        if not weapon:
            print(f"❌ 무기를 찾을 수 없습니다: {weapon_id}")
            return False
        
        # 직업 제한 확인
        if not weapon.can_be_used_by(player.job):
            print(f"❌ {player.job}은(는) {weapon.name}을(를) 사용할 수 없습니다.")
            return False
        
        # 금액 확인 (향후 Player에 money 필드 추가 시 활성화)
        # if player.money < weapon.price:
        #     print(f"❌ 금액이 부족합니다. 필요: {weapon.price}전, 보유: {player.money}전")
        #     return False
        
        # 인벤토리 용량 확인
        if not player.inventory.can_add_item():
            print("❌ 인벤토리가 가득 차서 무기를 구매할 수 없습니다.")
            return False
        
        # 구매 처리 (향후 인벤토리에 무기 추가 기능 구현)
        print(f"✅ {weapon.name}을(를) {weapon.price}전에 구매했습니다!")
        
        # 바로 장착할지 묻기
        choice = input(f"🔄 {weapon.name}을(를) 바로 장착하시겠습니까? (y/n): ").lower().strip()
        if choice in ['y', 'yes', '예', 'ㅇ']:
            player.equip_weapon(weapon)
        
        return True


class ShopSystem:
    """상점 관리 시스템"""
    
    def __init__(self):
        self.shops: Dict[str, Shop] = {}
        self.load_shops()
    
    def load_shops(self):
        """shops.json에서 상점 데이터를 로드합니다."""
        shop_file = os.path.join("data", "shops.json")
        
        if not os.path.exists(shop_file):
            print("⚠️ shops.json 파일이 없습니다.")
            return
        
        try:
            with open(shop_file, 'r', encoding='utf-8') as file:
                shop_data_dict = json.load(file)
            
            # 상점 객체 생성 및 저장
            for shop_id, shop_data in shop_data_dict.items():
                shop_data['id'] = shop_id
                shop = Shop(shop_data)
                self.shops[shop_id] = shop
            
            print(f"✅ {len(self.shops)}개의 상점을 로드했습니다.")
            
        except Exception as e:
            print(f"❌ 상점 데이터 로드 실패: {e}")
    
    def get_shop(self, shop_id: str) -> Optional[Shop]:
        """상점 ID로 상점을 조회합니다."""
        return self.shops.get(shop_id)
    
    def get_shop_by_npc(self, npc_name: str) -> Optional[Shop]:
        """NPC 이름으로 상점을 조회합니다."""
        for shop in self.shops.values():
            if shop.npc_name == npc_name:
                return shop
        return None
    
    def get_shops_by_region(self, region: str) -> List[Shop]:
        """지역별 상점 목록을 반환합니다."""
        return [shop for shop in self.shops.values() if shop.region == region]
    
    def show_all_shops(self):
        """모든 상점 목록을 표시합니다."""
        print("\n🏪 **전체 상점 목록**")
        print("=" * 50)
        
        # 지역별로 그룹화
        shops_by_region = {}
        for shop in self.shops.values():
            if shop.region not in shops_by_region:
                shops_by_region[shop.region] = []
            shops_by_region[shop.region].append(shop)
        
        for region, shops in shops_by_region.items():
            print(f"\n📍 **{region}**")
            print("-" * 20)
            for shop in shops:
                print(f"🏪 {shop.name} (상인: {shop.npc_name})")
    
    def visit_shop(self, player, shop_id: str):
        """상점을 방문하고 상호작용합니다."""
        shop = self.get_shop(shop_id)
        if not shop:
            print(f"❌ 상점을 찾을 수 없습니다: {shop_id}")
            return
        
        shop.show_shop_info()
        
        while True:
            print("\n🛒 **무엇을 하시겠습니까?**")
            print("1. 소비 아이템 보기")
            print("2. 무기 보기")
            print("3. 아이템 구매")
            print("4. 무기 구매")
            print("5. 상점 나가기")
            
            choice = input("선택: ").strip()
            
            if choice == "1":
                shop.show_items()
            
            elif choice == "2":
                shop.show_weapons(player.job)
            
            elif choice == "3":
                shop.show_items()
                if shop.items:
                    item_name = input("\n구매할 아이템 이름: ").strip()
                    shop.buy_item(player, item_name)
            
            elif choice == "4":
                shop.show_weapons(player.job)
                if shop.weapons:
                    print("\n무기 ID 목록:")
                    for i, weapon_id in enumerate(shop.weapons, 1):
                        weapon = shop.weapon_system.get_weapon(weapon_id)
                        if weapon:
                            print(f"{i}. {weapon_id} - {weapon.name}")
                    
                    try:
                        weapon_idx = int(input("구매할 무기 번호: ")) - 1
                        if 0 <= weapon_idx < len(shop.weapons):
                            weapon_id = shop.weapons[weapon_idx]
                            shop.buy_weapon(player, weapon_id)
                        else:
                            print("❌ 잘못된 번호입니다.")
                    except ValueError:
                        print("❌ 숫자를 입력해주세요.")
            
            elif choice == "5":
                print("🚪 상점을 나갑니다.")
                break
            
            else:
                print("❌ 잘못된 선택입니다.")


def test_shop_system():
    """상점 시스템 테스트 함수"""
    print("🧪 상점 시스템 테스트 시작")
    print("=" * 40)
    
    # 상점 시스템 초기화
    shop_system = ShopSystem()
    
    # 전체 상점 목록
    shop_system.show_all_shops()
    
    # 특정 상점 테스트
    shop = shop_system.get_shop("shop_001")
    if shop:
        print(f"\n🧪 {shop.name} 테스트")
        shop.show_shop_info()
        shop.show_items()
        shop.show_weapons("도사")
    
    print("\n✅ 상점 시스템 테스트 완료!")


if __name__ == "__main__":
    test_shop_system() 