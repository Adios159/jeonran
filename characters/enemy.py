from characters.base_character import BaseCharacter
import random

class Enemy(BaseCharacter):
    def __init__(self, name, max_hp, attack, defence, speed, exp_reward, status_chance=None):
        super().__init__(name, max_hp, attack, defence, speed)
        self.exp_reward = exp_reward
        self.status_chance = status_chance or {}

    def choose_action(self, target):
        print(f"{self.name}이(가) 공격을 시도합니다!")
        self.attack_target(target)
        for status, chance in self.status_chance.items():
            if random.random() < chance:
                target.apply_status(status, 3)