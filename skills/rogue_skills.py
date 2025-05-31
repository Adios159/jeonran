from skills.base_skill import Skill

def quick_stab(user, target):
    damage = int(user.attack * 1.3 - target.defence)
    damage = max(1, int(damage))
    target.current_hp -= damage
    print(f"{target.name}에게 날렵한 단검으로 {damage}의 피해를 입혔다")

def poison_dagger(user, target):
    damage = int(user.attack - target.defence)
    damage = max(1, int(damage))
    target.current_hp -= damage
    print(f"{target.name}에게 독 단검으로 {damage}의 피해를 입혔다")

warrior_skills = [
    Skill(
        name = "화염구",
        description = "화상 상태이상을 줄 수 있는 마법",
        mp_cost = 6,
        effect_func = quick_stab,
        ),
    Skill(
        name = "방패 가격",
        description = "적을 방패로 가격하여 스텀 상태이상을 유발 할 수 있다",
        mp_cost=4,
        effect_func=poison_dagger,
        status_effect="poison",
        status_chance = 0.4
    )
]