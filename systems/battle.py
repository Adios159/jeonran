from skills.base_skill import Skill
import random

def start_battle(player, enemies):
    """전투 시스템 - 1-3마리 몬스터와의 전투 지원"""
    # 단일 몬스터를 리스트로 변환 (기존 호환성)
    if not isinstance(enemies, list):
        enemies = [enemies]
    
    print("\n--- 전투 시작 ---")
    if len(enemies) == 1:
        print(f"{enemies[0].name}이(가) 나타났다")
    else:
        print(f"{len(enemies)}마리의 요괴와 전투가 시작되었다!")

    while player.is_alive() and any(enemy.is_alive() for enemy in enemies):
        print("\n[플레이어 턴]")
        max_mp = 30 + 5 * (player.level - 1)
        print(f"{player.name} (HP: {player.current_hp}/{player.max_hp}, MP:{player.mp}/{max_mp})")
        
        # 살아있는 적들만 표시
        alive_enemies = [enemy for enemy in enemies if enemy.is_alive()]
        print("적 상태:")
        for i, enemy in enumerate(alive_enemies, 1):
            print(f"  {i}. {enemy.display_name} (HP: {enemy.current_hp}/{enemy.max_hp})")

        # 플레이어 행동 불가 상태 체크
        if not player.can_act():
            if "freeze" in player.status_effects:
                print(f"{player.name}은(는) 빙결 상태로 행동할 수 없다!")
            elif "stun" in player.status_effects:
                print(f"{player.name}은(는) 기절 상태로 행동할 수 없다!")
        else:
            # 플레이어 행동 선택
            action_result = player_turn(player, alive_enemies)
            if action_result == "escaped":
                return "player_escaped"
        
        # 죽은 적들 확인
        alive_enemies = [enemy for enemy in enemies if enemy.is_alive()]
        if not alive_enemies:
            print(f"모든 요괴를 쓰러뜨렸다!")
            return "player_victory"

        print("\n[적 턴]")
        # 살아있는 적들의 행동
        for enemy in alive_enemies:
            if not enemy.can_act():
                if "freeze" in enemy.status_effects:
                    print(f"{enemy.display_name}은(는) 빙결 상태로 행동할 수 없다!")
                elif "stun" in enemy.status_effects:
                    print(f"{enemy.display_name}은(는) 기절 상태로 행동할 수 없다!")
            else:
                print(f"\n{enemy.display_name}의 턴:")
                enemy.choose_action(player)
                
                # 플레이어가 죽었는지 확인
                if not player.is_alive():
                    print("\n당신은 패배하였습니다...")
                    return "player_defeat"

        # 턴 종료 처리
        player.end_turn()
        for enemy in alive_enemies:
            enemy.end_turn()

    # 전투 루프가 끝났을 때의 최종 결과
    if not player.is_alive():
        return "player_defeat"
    elif not any(enemy.is_alive() for enemy in enemies):
        return "player_victory"
    else:
        return "unknown"  # 이론적으로 도달하지 않아야 함

def player_turn(player, alive_enemies):
    """플레이어 턴 처리 - 다중 몬스터 대응"""
    print("\n행동을 선택하세요")
    print("1. 공격")
    print("2. 스킬 사용")
    print("3. 아이템 사용")
    print("4. 도망")
    
    choice = input("> ")

    if choice == "1":
        # 공격할 대상 선택
        target = select_target(alive_enemies)
        if target:
            player.attack_target(target)

    elif choice == "2":
        # 스킬 사용
        target = None
        if len(alive_enemies) > 1:
            target = select_target(alive_enemies)
        else:
            target = alive_enemies[0]
            
        if target and use_skill(player, target):
            pass  # 스킬 사용 성공
        else:
            # 스킬 사용 실패 시 기본 공격
            if target:
                player.attack_target(target)

    elif choice == "3":
        if use_item(player):
            pass  # 아이템 사용 성공
        else:
            # 아이템 사용 실패 시 턴을 다시 진행
            return player_turn(player, alive_enemies)

    elif choice == "4":
        # 도망 시스템 - 가장 빠른 적 기준으로 계산
        fastest_enemy_speed = max(enemy.speed for enemy in alive_enemies)
        escape_chance = min(0.8, player.speed / (player.speed + fastest_enemy_speed) + 0.3)
        
        if random.random() < escape_chance:
            print(f"{player.name}이(가) 성공적으로 도망쳤다!")
            return "escaped"
        else:
            print(f"{player.name}이(가) 도망치려 했지만 실패했다!")

    else:
        print("잘못된 입력입니다. 기본 공격을 진행합니다.")
        target = select_target(alive_enemies)
        if target:
            player.attack_target(target)
    
    return "continue"

def select_target(alive_enemies):
    """공격할 대상 선택"""
    if len(alive_enemies) == 1:
        return alive_enemies[0]
    
    print("\n공격할 대상을 선택하세요:")
    for i, enemy in enumerate(alive_enemies, 1):
        print(f"{i}. {enemy.display_name} (HP: {enemy.current_hp}/{enemy.max_hp})")
    print("0. 취소")
    
    try:
        target_choice = int(input("> "))
        if target_choice == 0:
            return None
        elif 1 <= target_choice <= len(alive_enemies):
            return alive_enemies[target_choice - 1]
        else:
            print("잘못된 번호입니다. 첫 번째 적을 자동 선택합니다.")
            return alive_enemies[0]
    except ValueError:
        print("숫자를 입력해 주세요. 첫 번째 적을 자동 선택합니다.")
        return alive_enemies[0]

def use_skill(player, target):
    """스킬 사용 처리"""
    skills = player.skills
    
    print("사용할 스킬을 선택하세요:")
    for i, skill in enumerate(skills):
        print(f"{i+1}. {skill.name} (MP: {skill.mp_cost}) - {skill.description}")
    print("0. 취소")
    
    skill_choice = input("> ")

    if skill_choice == "0":
        return False
    
    try:
        skill_index = int(skill_choice) - 1
        if 0 <= skill_index < len(skills):
            selected_skill = skills[skill_index]
            return selected_skill.use(player, target)
        else:
            print("올바르지 않은 번호입니다.")
            return False
    except ValueError:
        print("숫자를 입력해 주세요.")
        return False

def use_item(player):
    """아이템 사용 처리"""
    # 인벤토리가 비어있는지 확인
    if player.inventory.is_empty():
        print("사용할 수 있는 아이템이 없습니다.")
        return False
    
    # 아이템 목록 표시
    item_list = player.inventory.list_items()
    
    print("\n사용할 아이템을 선택하세요:")
    print("0. 취소")
    
    item_choice = input("> ")
    
    if item_choice == "0":
        print("아이템 사용을 취소했습니다.")
        return False
    
    try:
        item_index = int(item_choice) - 1
        if 0 <= item_index < len(item_list):
            selected_item = item_list[item_index]
            return player.use_item(selected_item)
        else:
            print("올바르지 않은 번호입니다.")
            return False
    except ValueError:
        print("숫자를 입력해 주세요.")
        return False
