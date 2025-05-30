def start_battle(player, enemy):
    print("\n--- 전투 시작 ---")
    print(f"{enemy.name}이(가) 나타났다")

    while player.is_alive() and enemy.is_alive():
        print("\n[플레이어 턴]")
        print(f"{player.name} (HP: {player.current_hp}/{player.max_hp}, MP:{player.mp})")
        print(f"{enemy.name} (HP: {enemy.current_hp}/{enemy.max_hp})")

        print("\n행동을 선택하세요")
        print("1. 공격")
        print("2. 스킬 사용(미구현)")
        print("3. 아이템 사용(미구현)")
        print("4. 도망(미구현)")
        
        choice = input("> ")

        if choice == "1":
            player.attack_target(enemy)
        elif choice == "2":
            print("스킬 시스템은 아직 구현되지 않았습니다")
        elif choice == "3":
            print("아이템 시스템은 아직 구현되지 않았습니다")
        elif choice == "4":
            print("도망 시스템은 아직 구현되지 않았습니다")
        else:
            print("잘못된 입력 입니다. 기본 공격을 진행합니다")
            player.attack_target(enemy)

        if not enemy.is_alive():
            print(f"{enemy.name}을(를) 쓰러뜨렸다")
            print(f"경험치 {enemy.exp_reward} 획득!")
            player.exp += enemy.exp_reward
            return
        
        print("\n[적 턴]")
        enemy.choose_action(player)

        player.end_turn()
        enemy.end_turn()
    
    if not player.is_alive():
        print("\n당신은 패배하였습니다...")