from skills.base_skill import Skill

def fireball(user, target):
    damage = int(user.attack * 1.2 + 10 - target.defence)
    damage = max(1, int(damage))
    target.current_hp -= damage
    print(f"{target.name}에게 불덩이를 날려 {damage}의 피해를 입혔다")

def frost_wave(user, target):
    damage = int(user.attack * 0.8 + 5 - target.defence)
    damage = max(1, int(damage))
    target.current_hp -= damage
    print(f"{target.name}에게 냉기를 날려 {damage}의 피해를 입혔다")

mage_skills = [
    Skill(
        name = "화염구",
        description = "화상 상태이상을 줄 수 있는 마법",
        mp_cost = 6,
        effect_func = fireball,
        status_effect = "burn",
        status_chance =0.3
        ),
    Skill(
        name = "방패 가격",
        description = "적을 방패로 가격하여 스텀 상태이상을 유발 할 수 있다",
        mp_cost=4,
        effect_func=frost_wave,
        status_effect="freeze",
        status_chance = 0.3
    )
]