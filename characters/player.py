from characters.base_character import BaseCharacter
from skills.warrior_skills import warrior_skills
from skills.mage_skills import mage_skills
from skills.rogue_skills import rogue_skills

class Player(BaseCharacter):
    def __init__(self, name, job):
        self.job = job

        if job == "무사":
            max_hp = 120
            attack = 18
            defence = 15
            speed = 8
            skills = ["가르기"]

        elif job == "도사":
            max_hp = 80
            attack = 12
            defence = 8
            speed = 10
            skills = ["화염부"]

        elif job == "유랑객":
            max_hp = 90
            attack = 14
            defence = 10
            speed = 18
            skills = ["급소찌르기"]

        else:
            raise ValueError("없는 직업 입니다.")
        
        super().__init__(name, max_hp, attack, defence, speed)

        self.level = 1
        self.exp = 0
        self.mp = 30

        # 직업별 스킬 할당
        if job == "무사":
            self.skills = warrior_skills
        elif job == "도사":
            self.skills = mage_skills
        elif job == "유랑객":
            self.skills = rogue_skills
        else:
            raise ValueError("없는 직업 입니다")
    
    def end_turn(self):
        # 부모 클래스의 상태이상 처리
        super().end_turn()
        
        # MP 회복 (턴당 2 회복, 최대치 초과 불가)
        max_mp = 30 + 5 * (self.level - 1)  # 레벨당 MP 5 증가
        old_mp = self.mp
        self.mp = min(self.mp + 2, max_mp)
        if self.mp > old_mp:
            print(f"{self.name}의 마력이 {self.mp - old_mp}만큼 회복되었다 (MP: {self.mp}/{max_mp})")
    
    def gain_exp(self, amount):
        """경험치 획득 및 레벨업 처리"""
        self.exp += amount
        print(f"경험치 {amount} 획득! (총 경험치: {self.exp})")
        
        # 레벨업 체크 (경험치 100마다 레벨업)
        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level += 1
            
            # 레벨업 보상
            hp_increase = 10
            attack_increase = 2
            defence_increase = 1
            mp_increase = 5
            
            self.max_hp += hp_increase
            self.current_hp += hp_increase  # 레벨업 시 HP도 회복
            self.attack += attack_increase
            self.defence += defence_increase
            
            print(f"\n🎉 레벨업! {self.level-1} → {self.level}")
            print(f"HP +{hp_increase} (최대 HP: {self.max_hp})")
            print(f"공격력 +{attack_increase} (현재: {self.attack})")
            print(f"방어력 +{defence_increase} (현재: {self.defence})")
            print(f"최대 MP +{mp_increase} (현재: 30 + {mp_increase * (self.level-1)})")
            
            # MP 최대치도 증가
            max_mp = 30 + mp_increase * (self.level - 1)
            self.mp = min(self.mp + mp_increase, max_mp)