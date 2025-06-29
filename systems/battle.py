from skills.base_skill import Skill

def start_battle(player, enemy):
    print("\n--- 전투 시작 ---")
    print(f"{enemy.name}이(가) 나타났다")

    while player.is_alive() and enemy.is_alive():
        print("\n[플레이어 턴]")
        max_mp = 30 + 5 * (player.level - 1)
        print(f"{player.name} (HP: {player.current_hp}/{player.max_hp}, MP:{player.mp}/{max_mp})")
        print(f"{enemy.name} (HP: {enemy.current_hp}/{enemy.max_hp})")

        # 플레이어 행동 불가 상태 체크
        if not player.can_act():
            if "freeze" in player.status_effects:
                print(f"{player.name}은(는) 빙결 상태로 행동할 수 없다!")
            elif "stun" in player.status_effects:
                print(f"{player.name}은(는) 기절 상태로 행동할 수 없다!")
        else:
            print("\n행동을 선택하세요")
            print("1. 공격")
            print("2. 스킬 사용")
            print("3. 아이템 사용")
            print("4. 도망")
            
            choice = input("> ")

            if choice == "1":
                player.attack_target(enemy)

            elif choice == "2":
                skills = player.skills
                while True:
                    print("사용할 스킬을 선택하세요:")
                    for i, skill in enumerate(skills):
                        print(f"{i+1}. {skill.name} (MP: {skill.mp_cost}) - {skill.description}")
                    skill_choice = input("> ")
        
                    try:
                        skill_index = int(skill_choice) - 1
                        if 0 <= skill_index < len(skills):
                            selected_skill = skills[skill_index]
                            selected_skill.use(player, enemy)
                            break
                        else:
                            print("올바르지 않은 번호입니다.")
                    except ValueError:
                        print("숫자를 입력해 주세요.")

            elif choice == "3":
                # 인벤토리가 비어있는지 확인
                if player.inventory.is_empty():
                    print("사용할 수 있는 아이템이 없습니다.")
                else:
                    # 아이템 목록 표시
                    item_list = player.inventory.list_items()
                    
                    print("\n사용할 아이템을 선택하세요:")
                    print("0. 취소")
                    
                    item_choice = input("> ")
                    
                    if item_choice == "0":
                        print("아이템 사용을 취소했습니다.")
                        continue  # 다시 행동 선택으로
                    
                    try:
                        item_index = int(item_choice) - 1
                        if 0 <= item_index < len(item_list):
                            selected_item = item_list[item_index]
                            if player.use_item(selected_item):
                                # 아이템 사용 성공 시에만 턴 진행
                                pass
                            else:
                                # 아이템 사용 실패 시 다시 선택
                                continue
                        else:
                            print("올바르지 않은 번호입니다.")
                            continue
                    except ValueError:
                        print("숫자를 입력해 주세요.")
                        continue

            elif choice == "4":
                # 도망 시스템 구현
                import random
                escape_chance = min(0.8, player.speed / (player.speed + enemy.speed) + 0.3)
                
                if random.random() < escape_chance:
                    print(f"{player.name}이(가) 성공적으로 도망쳤다!")
                    return
                else:
                    print(f"{player.name}이(가) 도망치려 했지만 실패했다!")

            else:
                print("잘못된 입력입니다. 기본 공격을 진행합니다.")
                player.attack_target(enemy)

        if not enemy.is_alive():
            print(f"{enemy.name}을(를) 쓰러뜨렸다")
            player.gain_exp(enemy.exp_reward)
            return

        print("\n[적 턴]")
        # 적도 행동 불가 상태 체크
        if not enemy.can_act():
            if "freeze" in enemy.status_effects:
                print(f"{enemy.name}은(는) 빙결 상태로 행동할 수 없다!")
            elif "stun" in enemy.status_effects:
                print(f"{enemy.name}은(는) 기절 상태로 행동할 수 없다!")
        else:
            enemy.choose_action(player)

        player.end_turn()
        enemy.end_turn()

    if not player.is_alive():
        print("\n당신은 패배하였습니다...")
