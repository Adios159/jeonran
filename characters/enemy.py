from characters.base_character import BaseCharacter
import random

class Enemy(BaseCharacter):
    def __init__(self, name, max_hp, attack, defence, speed, exp_reward, status_chance=None):
        super().__init__(name, max_hp, attack, defence, speed)
        self.exp_reward = exp_reward
        self.status_chance = status_chance or {}
        
        # Monster 시스템과 호환을 위한 추가 속성들
        self.description = ""
        self.skill = ""
        self.regions = []
        self.special_traits = {}
        self.trait_type = "normal"
        self.display_name = name  # 다중 전투에서 구별용

    def choose_action(self, target):
        display_name = getattr(self, 'display_name', self.name)
        print(f"{display_name}이(가) 공격을 시도합니다!")
        self.attack_target(target)
        for status, chance in self.status_chance.items():
            if random.random() < chance:
                target.apply_status(status, 3)