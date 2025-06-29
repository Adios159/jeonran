class BaseCharacter:
    def __init__(self, name, max_hp, attack, defence, speed):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.status_effects = {}

    def is_alive(self):
        return self.current_hp > 0
    
    def can_act(self):
        """행동 가능 여부 확인"""
        # 빙결이나 기절 상태일 때 행동 불가
        return not ("freeze" in self.status_effects or "stun" in self.status_effects)
    
    def take_damage(self, amount):
        reduced = max(1, amount - self.defence)
        self.current_hp = max(0, self.current_hp - reduced)
        print(f"{self.name}이(가) {reduced}의 패히를 입었다! (남은 HP:{self.current_hp})")

    def apply_status(self, status, duration):
        if status not in self.status_effects:
            self.status_effects[status] = duration
            print(f"{self.name}은(는) {status} 상태이상에 걸렸다!")

    def end_turn(self):
        to_remove = []
        for status in self.status_effects:
            # 상태이상 효과 적용
            if status == "burn":
                damage = max(1, int(self.max_hp * 0.1))  # 최대 HP의 10%
                self.current_hp = max(0, self.current_hp - damage)
                print(f"{self.name}이(가) 화상으로 {damage}의 피해를 입었다!")
            elif status == "poison":
                damage = max(1, int(self.max_hp * 0.08))  # 최대 HP의 8%
                self.current_hp = max(0, self.current_hp - damage)
                print(f"{self.name}이(가) 독으로 {damage}의 피해를 입었다!")
            elif status == "freeze":
                print(f"{self.name}은(는) 빙결 상태로 행동할 수 없다!")
            elif status == "stun":
                print(f"{self.name}은(는) 기절 상태로 행동할 수 없다!")
            
            # 지속시간 감소
            self.status_effects[status] -= 1
            if self.status_effects[status] <= 0:
                to_remove.append(status)
        
        for status in to_remove:
            print(f"{self.name}의 {status} 상태이상이 해제되었다")
            del self.status_effects[status]
    def attack_target(self,target):
        print(f"{self.name}이(가) {target.name}을(를) 공격했다")
        target.take_damage(self.attack)