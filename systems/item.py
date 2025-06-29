class Item:
    def __init__(self, name, description, item_type="misc"):
        self.name = name
        self.description = description
        self.item_type = item_type

    def use(self, user):
        """기본 아이템 사용 - 하위 클래스에서 오버라이드"""
        print(f"{self.name}을(를) 사용할 수 없습니다.")
        return False

class HealingItem(Item):
    def __init__(self, name, description, heal_amount, heal_type="hp"):
        super().__init__(name, description, "healing")
        self.heal_amount = heal_amount
        self.heal_type = heal_type

    def use(self, user):
        if self.heal_type == "hp":
            if user.current_hp >= user.max_hp:
                print(f"{user.name}의 체력이 이미 가득합니다.")
                return False
            
            old_hp = user.current_hp
            user.current_hp = min(user.current_hp + self.heal_amount, user.max_hp)
            healed = user.current_hp - old_hp
            
            print(f"{user.name}이(가) {self.name}을(를) 사용하여 체력을 {healed} 회복했다!")
            print(f"현재 HP: {user.current_hp}/{user.max_hp}")
            return True
            
        elif self.heal_type == "mp":
            max_mp = 30 + 5 * (user.level - 1)
            if user.mp >= max_mp:
                print(f"{user.name}의 마력이 이미 가득합니다.")
                return False
            
            old_mp = user.mp
            user.mp = min(user.mp + self.heal_amount, max_mp)
            recovered = user.mp - old_mp
            
            print(f"{user.name}이(가) {self.name}을(를) 사용하여 마력을 {recovered} 회복했다!")
            print(f"현재 MP: {user.mp}/{max_mp}")
            return True

# 기본 회복 아이템들 정의
healing_herb = HealingItem(
    name="소형 약초",
    description="체력을 25 회복시켜주는 기본적인 약초",
    heal_amount=25,
    heal_type="hp"
)

large_healing_herb = HealingItem(
    name="대형 약초", 
    description="체력을 50 회복시켜주는 강력한 약초",
    heal_amount=50,
    heal_type="hp"
)

mana_potion = HealingItem(
    name="마력 물약",
    description="마력을 15 회복시켜주는 물약",
    heal_amount=15,
    heal_type="mp"
)

# 아이템 목록
basic_items = {
    "소형 약초": healing_herb,
    "대형 약초": large_healing_herb,
    "마력 물약": mana_potion
}
