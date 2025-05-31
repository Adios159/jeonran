class Skill:
    def __init__(self, name, description, mp_cost, effect_func, status_effect=None, status_chance=0.0):
        self.name = name
        self.description = description
        self.mp_cost = mp_cost
        self.effect_func = effect_func
        self.status_effect = status_effect
        self.status_chance = status_chance
        def use(self, user, target):
            if user.mp < self.mp_cost:
                print(f"{user.name}의 마력이 부족하여 {self.name}을 쓸 수 없소")
                return False
            
            user.mp -= self.mp_cost
            print(f"{user.name}이(가) {self.name}을(를) 사용하였다!")
            self.effect_func(user, target)

            import random
            if self.status_effect and random.random() < self.status_chance:
                target.apply_status(self.status_effect, 3)
                print(f"{target.name}이(가) {self.status_effect} 상태이상에 걸렸다")
                return False