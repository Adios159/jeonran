from skills.base_skill import Skill

def quick_stab(user, target):
    """급소 찔러내기 - 1.3배 치명타 피해"""
    damage = int(user.attack * 1.3)
    target.take_damage(damage)

def poison_dagger(user, target):
    """독 단검 - 기본 피해 + 독 상태이상"""
    damage = user.attack
    target.take_damage(damage)

rogue_skills = [
    Skill(
        name = "급소 찔러내기",
        description = "적의 급소를 노려 높은 피해를 입힌다",
        mp_cost = 6,
        effect_func = quick_stab,
        ),
    Skill(
        name = "독 단검",
        description = "독 상태이상을 유발할 수 있다",
        mp_cost=4,
        effect_func=poison_dagger,
        status_effect="poison",
        status_chance = 0.4
    )
]