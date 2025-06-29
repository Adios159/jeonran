from typing import Dict, List, Optional
from systems.status_effect import StatusEffect, create_status_effect

class BaseCharacter:
    def __init__(self, name, max_hp, attack, defence, speed):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.status_effects: Dict[str, StatusEffect] = {}

    def is_alive(self):
        return self.current_hp > 0
    
    def can_act(self):
        """행동 가능 여부 확인"""
        # 모든 상태이상에 대해 행동 가능 여부 체크
        for effect in self.status_effects.values():
            if not effect.can_act():
                return False
        return True
    
    def take_damage(self, amount):
        """데미지를 받고 상태이상 처리"""
        reduced = max(1, amount - self.defence)
        self.current_hp = max(0, self.current_hp - reduced)
        print(f"{self.name}이(가) {reduced}의 피해를 입었다! (남은 HP:{self.current_hp})")
        
        # 피격 시 상태이상 처리 (예: 수면 해제)
        to_remove = []
        for effect_name, effect in self.status_effects.items():
            if effect.on_hit(self):
                to_remove.append(effect_name)
                print(f"{self.name}의 {effect_name} 상태가 해제되었다!")
        
        for effect_name in to_remove:
            del self.status_effects[effect_name]

    def apply_status(self, effect_type: str) -> bool:
        """상태이상 적용"""
        effect = create_status_effect(effect_type)
        if not effect:
            return False
            
        if effect_type in self.status_effects:
            # 이미 있는 상태이상이면 지속시간만 초기화
            self.status_effects[effect_type].extend_duration()
            print(f"{self.name}의 {effect_type} 상태가 연장되었다!")
        else:
            # 새로운 상태이상 추가
            self.status_effects[effect_type] = effect
            print(f"{self.name}에게 {effect.get_info()} 상태가 적용되었다!")
        return True

    def end_turn(self):
        """턴 종료 시 상태이상 처리"""
        to_remove = []
        
        # 모든 상태이상 효과 적용
        for effect_name, effect in self.status_effects.items():
            # 상태이상 효과 적용
            message = effect.apply_effect(self)
            if message:
                print(message)
            
            # 지속시간 감소
            if effect.decrease_duration():
                to_remove.append(effect_name)
        
        # 종료된 상태이상 제거
        for effect_name in to_remove:
            print(f"{self.name}의 {effect_name} 상태가 해제되었다!")
            del self.status_effects[effect_name]

    def get_status_effects_info(self) -> str:
        """현재 상태이상 정보 반환"""
        if not self.status_effects:
            return "상태이상 없음"
        
        return "\n".join(effect.get_description() for effect in self.status_effects.values())

    def attack_target(self, target):
        """대상 공격"""
        if not self.can_act():
            print(f"{self.name}은(는) 행동할 수 없다!")
            return
            
        print(f"{self.name}이(가) {target.name}을(를) 공격했다!")
        target.take_damage(self.attack)