from skills.base_skill import Skill

def powerful_slash(user, target):
    """강력한 베기 - 1.5배 피해"""
    damage = int(user.attack * 1.5)
    target.take_damage(damage)

def shield_bash(user, target):
    """방패 가격 - 0.8배 피해 + 기절 확률"""
    damage = int(user.attack * 0.8)
    target.take_damage(damage)

warrior_skills = [
    Skill(
        name = "강력한 베기",
        description = "적에게 강력한 베기를 날려 큰 피해를 준다",
        mp_cost = 5,
        effect_func = powerful_slash
    ),
    Skill(
        name = "방패 가격",
        description = "적을 방패로 가격하여 기절 상태이상을 유발할 수 있다",
        mp_cost=4,
        effect_func=shield_bash,
        status_effect="stun",
        status_chance = 0.3
    )
]