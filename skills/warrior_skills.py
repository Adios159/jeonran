from skills.base_skill import Skill

def powerful_slash(user, target):
    damage = int(user.attack * 1.5 - target.defence)
    damage = max(1, int(damage))
    target.current_hp -= damage
    print(f"{target.name}에게 {damage}의 피해를 입혔다")

def shild_bash(user, target):
    damage = int(user.attack * 0.8 - target.defence)
    damage = max(1, int(damage))
    target.current_hp -= damage
    print(f"{target.name}에게 {damage}의 피해를 입혔다")

warrior_skills = [
    Skill(
        name = "강력한 베기",
        description = "적에게 강력한 베기를 날려 큰 피해를 준다",
        mp_cost = 5,
        effect_func = powerful_slash
    ),
    Skill(
        name = "방패 가격",
        description = "적을 방패로 가격하여 스텀 상태이상을 유발 할 수 있다",
        mp_cost=4,
        effect_func=shild_bash,
        status_effect="stun",
        status_chance = 0.3
    )
]