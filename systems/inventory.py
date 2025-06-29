class Inventory:
    def __init__(self):
        self.items = {}      # {아이템_이름: 개수}
        self.weapons = []    # [무기_ID_목록] - 무기는 개별 관리
        self.max_capacity = 30  # 최대 30칸

    def add_item(self, item_name, quantity=1):
        """아이템 추가"""
        if not self.can_add_item(quantity):
            print(f"❌ 인벤토리 공간이 부족합니다. (필요: {quantity}칸, 여유: {self.get_available_capacity()}칸)")
            return False
        
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
        print(f"{item_name} {quantity}개를 획득했습니다!")
        return True

    def remove_item(self, item_name, quantity=1):
        """아이템 제거"""
        if item_name not in self.items:
            return False
        
        if self.items[item_name] < quantity:
            return False
        
        self.items[item_name] -= quantity
        if self.items[item_name] == 0:
            del self.items[item_name]
        return True

    def has_item(self, item_name, quantity=1):
        """아이템 보유 확인"""
        return self.items.get(item_name, 0) >= quantity

    def get_item_count(self, item_name):
        """아이템 개수 반환"""
        return self.items.get(item_name, 0)

    def list_items(self):
        """인벤토리 목록 출력"""
        if not self.items:
            print("인벤토리가 비어있습니다.")
            return []
        
        print("\n=== 인벤토리 ===")
        item_list = []
        for i, (item_name, quantity) in enumerate(self.items.items(), 1):
            print(f"{i}. {item_name} x{quantity}")
            item_list.append(item_name)
        return item_list

    def is_empty(self):
        """인벤토리 비어있는지 확인"""
        return len(self.items) == 0 and len(self.weapons) == 0
    
    def get_used_capacity(self):
        """현재 사용 중인 인벤토리 칸 수를 반환"""
        item_slots = sum(self.items.values())  # 소비 아이템은 개수만큼 칸 차지
        weapon_slots = len(self.weapons)       # 무기는 개당 1칸
        return item_slots + weapon_slots
    
    def get_available_capacity(self):
        """사용 가능한 인벤토리 칸 수를 반환"""
        return self.max_capacity - self.get_used_capacity()
    
    def can_add_item(self, quantity=1):
        """아이템을 추가할 수 있는지 확인"""
        return self.get_available_capacity() >= quantity
    
    def can_add_weapon(self, count=1):
        """무기를 추가할 수 있는지 확인"""
        return self.get_available_capacity() >= count
    
    def add_weapon(self, weapon_id):
        """무기를 인벤토리에 추가"""
        if not self.can_add_weapon():
            print("❌ 인벤토리가 가득 차서 무기를 추가할 수 없습니다.")
            return False
        
        self.weapons.append(weapon_id)
        print(f"⚔️ 무기를 인벤토리에 추가했습니다!")
        return True
    
    def remove_weapon(self, weapon_id):
        """무기를 인벤토리에서 제거"""
        if weapon_id in self.weapons:
            self.weapons.remove(weapon_id)
            return True
        return False
    
    def has_weapon(self, weapon_id):
        """특정 무기를 보유하고 있는지 확인"""
        return weapon_id in self.weapons
    
    def list_weapons(self):
        """보유 중인 무기 목록을 반환"""
        return self.weapons.copy()
    
    def show_inventory_status(self):
        """인벤토리 상태를 표시"""
        used = self.get_used_capacity()
        available = self.get_available_capacity()
        
        print(f"\n📦 **인벤토리 상태** ({used}/{self.max_capacity})")
        print(f"📊 사용 중: {used}칸 | 여유: {available}칸")
        
        if used >= self.max_capacity * 0.9:  # 90% 이상 찬 경우
            print("⚠️ 인벤토리가 거의 가득 찼습니다!")
        
        return used, available
    
    def show_detailed_inventory(self, weapon_system=None):
        """상세한 인벤토리 정보를 표시"""
        used, available = self.show_inventory_status()
        
        # 소비 아이템 표시
        if self.items:
            print("\n💊 **소비 아이템**")
            print("-" * 20)
            for item_name, quantity in self.items.items():
                print(f"  {item_name} x{quantity}")
        else:
            print("\n💊 소비 아이템이 없습니다.")
        
        # 무기 표시
        if self.weapons:
            print("\n⚔️ **무기**")
            print("-" * 20)
            for i, weapon_id in enumerate(self.weapons, 1):
                if weapon_system:
                    weapon = weapon_system.get_weapon(weapon_id)
                    if weapon:
                        print(f"  {i}. {weapon.get_rarity_color()} {weapon.name} (공격력: {weapon.attack})")
                    else:
                        print(f"  {i}. {weapon_id} (정보 없음)")
                else:
                    print(f"  {i}. {weapon_id}")
        else:
            print("\n⚔️ 무기가 없습니다.")
    
    def cleanup_items(self):
        """0개인 아이템들을 정리"""
        items_to_remove = [name for name, count in self.items.items() if count <= 0]
        for item_name in items_to_remove:
            del self.items[item_name]
