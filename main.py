from characters.player import Player
from characters.enemy import Enemy
from systems.battle import start_battle
from systems.monsters import monster_spawner
from systems.region import region_manager

def main():
    print("🌕 전란 그리고 요괴 🌕")
    name = input("당신의 이름을 알려주시오> ")

    print("\n직업을 선택하시오")
    print("1. 무사\n2. 도사\n3. 유랑객")
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
    
    print(f"\n환영합니다, {name}님!")
    print("모험을 시작하기 전 기본 아이템을 지급해드리겠습니다.")
    player.give_starting_items()

    # 현재 지역에서 랜덤 몬스터 소환
    current_region = region_manager.current_region
    print(f"\n현재 위치: {current_region}")
    print(region_manager.get_region_info())
    
    enemy = monster_spawner.get_random_monster(current_region)
    print(f"\n{current_region}에서 요괴의 기운이 느껴진다...")

    start_battle(player, enemy)

if __name__ == "__main__":
    main()