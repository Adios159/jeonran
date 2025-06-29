"""
전란 그리고 요괴 - 조선시대 RPG
파일: systems/status_effect.py
설명: 상태이상 시스템
"""
from typing import Dict, Optional, Callable
import random

__all__ = ["StatusEffect", "create_status_effect"]

class StatusEffect:
    """상태이상 클래스"""
    
    def __init__(self, name: str, duration: int, effect_func: Callable, 
                 description: str, icon: str, can_act_func: Optional[Callable] = None,
                 on_hit_func: Optional[Callable] = None):
        self.name = name
        self.duration = duration
        self.initial_duration = duration  # 초기 지속시간 저장
        self.effect_func = effect_func  # 매 턴 적용되는 효과
        self.description = description
        self.icon = icon
        self.can_act_func = can_act_func  # 행동 가능 여부 체크 함수
        self.on_hit_func = on_hit_func  # 피격 시 효과 함수
    
    def apply_effect(self, target) -> str:
        """상태이상 효과 적용"""
        if self.effect_func:
            return self.effect_func(target)
        return ""
    
    def can_act(self) -> bool:
        """행동 가능 여부 확인"""
        if self.can_act_func:
            return self.can_act_func()
        return True
    
    def on_hit(self, target) -> bool:
        """피격 시 처리"""
        if self.on_hit_func:
            return self.on_hit_func(target)
        return False
    
    def decrease_duration(self) -> bool:
        """지속시간 감소, 종료 여부 반환"""
        self.duration -= 1
        return self.duration <= 0
    
    def extend_duration(self):
        """지속시간 초기화 (같은 상태이상 중복 적용 시)"""
        self.duration = self.initial_duration
    
    def get_info(self) -> str:
        """상태이상 정보 반환"""
        return f"{self.icon} {self.name} ({self.duration}턴)"
    
    def get_description(self) -> str:
        """상태이상 설명 반환"""
        return f"{self.icon} {self.name}: {self.description} (남은 턴: {self.duration})"


def create_poison_effect() -> StatusEffect:
    """중독 상태이상 생성"""
    def poison_effect(target) -> str:
        damage = max(1, int(target.max_hp * 0.05))  # HP 5% 감소
        target.current_hp = max(0, target.current_hp - damage)
        return f"{target.name}이(가) 중독으로 {damage}의 피해를 입었다!"
    
    return StatusEffect(
        name="중독",
        duration=3,
        effect_func=poison_effect,
        description="매 턴 최대 HP의 5%만큼 피해를 입습니다",
        icon="☠️"
    )


def create_paralysis_effect() -> StatusEffect:
    """마비 상태이상 생성"""
    def paralysis_can_act() -> bool:
        return random.random() > 0.5  # 50% 확률로 행동 가능
    
    def paralysis_effect(target) -> str:
        if not paralysis_can_act():
            return f"{target.name}은(는) 마비로 인해 움직일 수 없다!"
        return ""
    
    return StatusEffect(
        name="마비",
        duration=2,
        effect_func=paralysis_effect,
        can_act_func=paralysis_can_act,
        description="50% 확률로 행동이 불가능해집니다",
        icon="⚡"
    )


def create_sleep_effect() -> StatusEffect:
    """수면 상태이상 생성"""
    def sleep_can_act() -> bool:
        return False  # 수면 중에는 항상 행동 불가
    
    def sleep_effect(target) -> str:
        return f"{target.name}은(는) 깊이 잠들어 있다..."
    
    def sleep_on_hit(target) -> bool:
        return True  # 공격 받으면 즉시 해제
    
    return StatusEffect(
        name="수면",
        duration=2,
        effect_func=sleep_effect,
        can_act_func=sleep_can_act,
        on_hit_func=sleep_on_hit,
        description="행동이 불가능하며, 공격받으면 즉시 해제됩니다",
        icon="💤"
    )


def create_status_effect(effect_type: str) -> Optional[StatusEffect]:
    """상태이상 생성 헬퍼 함수"""
    creators = {
        "poison": create_poison_effect,
        "paralysis": create_paralysis_effect,
        "sleep": create_sleep_effect
    }
    creator = creators.get(effect_type.lower())
    if creator:
        return creator()
    return None
