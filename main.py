from characters.player import Player
from characters.enemy import Enemy
from systems.battle import start_battle
from systems.monsters import monster_spawner
from systems.region import region_manager

def display_game_menu():
    """메인 게임 메뉴 출력"""
    print("\n" + "="*50)
    print("🌕 전란 그리고 요괴 🌕")
    print("="*50)
    print("1. 지역 탐험 (요괴와 전투)")
    print("2. 지역 이동")
    print("3. 사람들과 대화")
    print("4. 장비 관리 🆕")
    print("5. 현재 상태 확인")
    print("6. 지역 정보 보기")
    print("7. 요괴 도감")
    print("8. 휴식 (HP/MP 회복)")
    print("9. 게임 종료")
    print("="*50)

def rest_at_location(player):
    """지역에서 휴식 (한양에서만 완전 회복)"""
    current_region = region_manager.get_current_region_data()
    
    if current_region["features"].get("거점") or current_region["features"].get("여관"):
        # 안전한 지역에서 완전 회복
        player.current_hp = player.max_hp
        max_mp = 30 + 5 * (player.level - 1)
        player.mp = max_mp
        print(f"\n{current_region['name']}에서 푹 쉬었습니다.")
        print("체력과 마력이 완전히 회복되었습니다!")
        
        # 온천 보너스 (가마뫼)
        if current_region["features"].get("온천"):
            bonus_mp = int(max_mp * 0.5)
            player.mp = min(player.mp + bonus_mp, max_mp)
            print(f"온천의 효과로 마력이 추가로 {bonus_mp} 회복되었습니다!")
    else:
        # 일반 지역에서는 부분 회복
        heal_amount = max(10, player.max_hp // 4)
        player.current_hp = min(player.current_hp + heal_amount, player.max_hp)
        mp_recovery = 5
        max_mp = 30 + 5 * (player.level - 1)
        player.mp = min(player.mp + mp_recovery, max_mp)
        
        print(f"\n{current_region['name']}에서 잠시 쉬었습니다.")
        print(f"체력 {heal_amount} 회복, 마력 {mp_recovery} 회복")
        
        # 위험 지역에서는 휴식 중에도 위험 요소
        if current_region["features"].get("위험도") in ["높음", "매우높음", "극도로높음"]:
            import random
            if random.random() < 0.3:
                print("⚠️ 휴식 중 요괴의 기운이 느껴집니다...")

def explore_region(player):
    """현재 지역 탐험 (요괴와 전투)"""
    current_region = region_manager.current_region
    print(f"\n{current_region}을(를) 탐험합니다...")
    
    # 지역 설명 출력
    region_data = region_manager.get_current_region_data()
    print(region_data['description'])
    
    # 요괴 스폰 (1-3마리)
    enemies = monster_spawner.get_random_monsters(current_region)
    if not enemies:
        print("이곳은 평화로워 보입니다...")
        return True
    
    # 몬스터 출현 메시지
    if len(enemies) == 1:
        enemy = enemies[0]
        print(f"\n💀 {enemy.name}이(가) 나타났다!")
        description = getattr(enemy, 'description', '신비로운 요괴가 나타났다!')
        print(f"   {description}")
    else:
        print(f"\n💀💀 {len(enemies)}마리의 요괴가 무리지어 나타났다!")
        for i, enemy in enumerate(enemies, 1):
            print(f"   {i}. {enemy.display_name}")
    
    # 전투 시작
    battle_result = start_battle(player, enemies)
    
    if battle_result == "player_victory":
        # 경험치 계산 (모든 몬스터 경험치 합산)
        total_base_exp = sum(enemy.exp_reward for enemy in enemies)
        exp_bonus = region_data["features"].get("경험치_보너스", 1.0)
        final_exp = int(total_base_exp * exp_bonus)
        
        if exp_bonus > 1.0:
            print(f"\n🌟 {current_region}의 특별한 기운으로 경험치가 {int((exp_bonus-1)*100)}% 추가!")
        
        player.gain_exp(final_exp)
        return True
    elif battle_result == "player_escaped":
        print("\n도망에 성공했습니다!")
        return True
    else:  # player_defeat
        print("\n💀 게임 오버...")
        print("요괴에게 패배했습니다. 다시 도전해보세요!")
        return False

def travel_menu(player):
    """지역 이동 메뉴"""
    print(f"\n현재 위치: {region_manager.current_region}")
    destinations = region_manager.get_available_destinations()
    
    if not destinations:
        print("이동할 수 있는 지역이 없습니다.")
        return
    
    print("\n이동 가능한 지역:")
    for i, dest in enumerate(destinations, 1):
        # 지역 정보 간단히 표시
        dest_data = region_manager.get_region_data(dest)
        danger = "안전"
        if dest_data and "features" in dest_data:
            danger = dest_data["features"].get("위험도", "안전")
        print(f"{i}. {dest} (위험도: {danger})")
    
    print("0. 취소")
    
    try:
        choice = int(input("\n이동할 지역 번호> "))
        if choice == 0:
            return
        elif 1 <= choice <= len(destinations):
            destination = destinations[choice - 1]
            success, message = region_manager.travel_to(destination)
            print(f"\n{message}")
            
            if success:
                print(f"\n=== {destination} ===")
                print(region_manager.get_region_info())
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해주세요.")

def equipment_menu(player):
    """장비 관리 메뉴"""
    while True:
        print("\n⚔️ **장비 관리**")
        print("=" * 30)
        print("1. 장착 중인 장비 확인")
        print("2. 무기 도감 보기")
        print("3. 인벤토리 확인")
        print("4. 무기 장착/해제")
        print("5. 무기 검색")
        print("0. 돌아가기")
        
        choice = input("\n선택> ").strip()
        
        if choice == "1":
            player.show_equipment_status()
        
        elif choice == "2":
            player.weapon_system.show_weapon_catalog(player.job)
        
        elif choice == "3":
            player.inventory.show_detailed_inventory(player.weapon_system)
        
        elif choice == "4":
            weapon_equip_menu(player)
        
        elif choice == "5":
            keyword = input("검색할 키워드를 입력하세요: ").strip()
            if keyword:
                player.search_weapons(keyword)
            else:
                player.search_weapons()  # 전체 사용 가능 무기 표시
        
        elif choice == "0":
            break
        
        else:
            print("❌ 잘못된 선택입니다.")

def weapon_equip_menu(player):
    """무기 장착/해제 메뉴"""
    print("\n⚔️ **무기 장착/해제**")
    print("1. 무기 해제")
    print("2. 무기 장착 (테스트용)")
    print("0. 돌아가기")
    
    choice = input("\n선택> ").strip()
    
    if choice == "1":
        player.unequip_weapon()
    
    elif choice == "2":
        # 테스트용: 무기 시스템에서 무기를 선택하여 장착
        usable_weapons = player.weapon_system.get_usable_weapons(player.job)
        if not usable_weapons:
            print("❌ 사용할 수 있는 무기가 없습니다.")
            return
        
        print("\n사용 가능한 무기:")
        for i, weapon in enumerate(usable_weapons, 1):
            print(f"{i}. {weapon.get_rarity_color()} {weapon.name} (공격력: {weapon.attack})")
        
        try:
            weapon_choice = int(input("\n장착할 무기 번호 (0=취소): "))
            if weapon_choice == 0:
                return
            elif 1 <= weapon_choice <= len(usable_weapons):
                selected_weapon = usable_weapons[weapon_choice - 1]
                player.equip_weapon(selected_weapon)
            else:
                print("❌ 잘못된 번호입니다.")
        except ValueError:
            print("❌ 숫자를 입력해주세요.")

def show_player_status(player):
    """플레이어 상태 출력"""
    max_mp = 30 + 5 * (player.level - 1)
    print(f"\n=== {player.name} ({player.job}) ===")
    print(f"레벨: {player.level}")
    print(f"경험치: {player.exp}/{player.level * 100}")
    print(f"체력: {player.current_hp}/{player.max_hp}")
    print(f"마력: {player.mp}/{max_mp}")
    print(f"공격력: {player.attack} | 방어력: {player.defence} | 속도: {player.speed}")
    
    # 장착 무기 정보
    if player.equipped_weapon:
        print(f"장착 무기: {player.equipped_weapon.name} (공격력: {player.equipped_weapon.get_effective_attack(player.job)})")
    else:
        print("장착 무기: 없음")
    
    # 상태이상 확인
    if player.status_effects:
        print("상태이상:", ", ".join([f"{status}({turns}턴)" for status, turns in player.status_effects.items()]))
    
    # 인벤토리 확인
    if player.inventory.items or player.inventory.weapons:
        print("\n=== 인벤토리 간단 보기 ===")
        if player.inventory.items:
            for item_name, quantity in player.inventory.items.items():
                print(f"- {item_name} × {quantity}")
        if player.inventory.weapons:
            print(f"- 무기 {len(player.inventory.weapons)}개")
        
        used, total = player.inventory.get_used_capacity(), player.inventory.max_capacity
        print(f"용량: {used}/{total}칸")
    else:
        print("\n인벤토리가 비어있습니다.")

def main_game_loop(player):
    """메인 게임 루프"""
    print(f"\n환영합니다, {player.name}님!")
    print("모험을 시작하기 전 기본 아이템을 지급해드리겠습니다.")
    player.give_starting_items()
    
    print(f"\n{region_manager.current_region}에서 모험이 시작됩니다!")
    print(region_manager.get_region_info())
    
    while True:
        display_game_menu()
        choice = input("\n선택> ")
        
        if choice == "1":  # 지역 탐험
            if not explore_region(player):
                # 게임 오버
                break
        
        elif choice == "2":  # 지역 이동
            travel_menu(player)
        
        elif choice == "3":  # 사람들과 대화
            region_manager.interact_with_npcs()
        
        elif choice == "4":  # 장비 관리 🆕
            equipment_menu(player)
        
        elif choice == "5":  # 현재 상태 확인
            show_player_status(player)
        
        elif choice == "6":  # 지역 정보 보기
            print(f"\n{region_manager.get_region_info()}")
            
            # 추가로 이 지역 요괴 정보도 표시
            monster_info = monster_spawner.get_region_monster_info(region_manager.current_region)
            print(f"\n{monster_info}")
        
        elif choice == "7":  # 요괴 도감
            monster_spawner.list_all_monsters()
        
        elif choice == "8":  # 휴식
            rest_at_location(player)
        
        elif choice == "9":  # 게임 종료
            print("\n게임을 종료합니다. 안녕히 가세요!")
            break
        
        else:
            print("잘못된 선택입니다.")
        
        # 플레이어가 죽었는지 확인
        if player.current_hp <= 0:
            print("\n💀 게임 오버...")
            print("체력이 0이 되었습니다. 다시 도전해보세요!")
            break

def main():
    print("🌕 전란 그리고 요괴 🌕")
    print("조선시대 양란 직후, 요괴와 원혼이 들끓는 혼란한 시대...")
    print("당신은 이 혼란을 수습할 영웅이 될 수 있을까요?\n")
    
    name = input("당신의 이름을 알려주시오> ")

    print("\n직업을 선택하시오")
    print("1. 무사 - 높은 체력과 방어력의 탱커형")
    print("2. 도사 - 균형잡힌 마법사형") 
    print("3. 유랑객 - 높은 속도의 어쌔신형")
    job_choice = input("> ")

    if job_choice == "1":
        job = "무사"
    elif job_choice == "2":
        job = "도사"
    elif job_choice == "3":
        job = "유랑객"
    else:
        print("잘못된 입력입니다. 기본값인 무사를 선택합니다.")
        job = "무사"

    player = Player(name, job)
    
    # 메인 게임 루프 시작
    main_game_loop(player)

if __name__ == "__main__":
    main()