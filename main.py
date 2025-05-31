from characters.player import Player
from characters.enemy import Enemy
from systems.battle import start_battle

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

    enemy = Enemy(
        name = "호롱불",
        max_hp=50,
        attack=10,
        defence=3,
        speed=5,
        exp_reward=30,
        status_chance={"burn": 0.4}
    )

    start_battle(player, enemy)

if __name__ == "__main__":
    main()