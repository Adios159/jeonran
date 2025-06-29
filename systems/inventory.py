class Inventory:
    def __init__(self):
        self.items = {}  # {아이템_이름: 개수}

    def add_item(self, item_name, quantity=1):
        """아이템 추가"""
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
        print(f"{item_name} {quantity}개를 획득했습니다!")

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
        return len(self.items) == 0
