from characters.base_character import BaseCharacter

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
        self.skills = skills
        self.mp = 30