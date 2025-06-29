from skills.base_skill import Skill

def fireball(user, target):
    """화염구 - 1.2배 피해 + 마법 추가 피해"""
    damage = int(user.attack * 1.2 + 10)
    target.take_damage(damage)

def frost_wave(user, target):
    """서리파동 - 0.8배 피해 + 마법 추가 피해"""
    damage = int(user.attack * 0.8 + 5)
    target.take_damage(damage)

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
        name = "서리파동",
        description = "빙결 상태이상을 줄 수 있는 마법",
        mp_cost=4,
        effect_func=frost_wave,
        status_effect="freeze",
        status_chance = 0.3
    )
]