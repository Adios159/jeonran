"""
몬스터 시스템 테스트 프로그램
"""
from systems.monsters import monster_spawner, monster_data, MonsterFactory
from systems.region import regions

def main():
    print("👹 조선시대 요괴 시스템 테스트")
    print("=" * 50)
    
    while True:
        print("\n=== 메뉴 ===")
        print("1. 모든 요괴 도감 보기")
        print("2. 지역별 요괴 정보")
        print("3. 랜덤 요괴 소환")
        print("4. 특정 요괴 정보")
        print("5. 지역별 요괴 출몰 현황")
        print("6. 종료")
        
        choice = input("\n선택> ")
        
        if choice == "1":
            monster_spawner.list_all_monsters()
        
        elif choice == "2":
            print("\n지역을 선택하세요:")
            region_list = list(regions.keys())
            for i, region in enumerate(region_list, 1):
                print(f"{i}. {region}")
            
            try:
                region_choice = int(input("지역 번호> ")) - 1
                if 0 <= region_choice < len(region_list):
                    region_name = region_list[region_choice]
                    print(f"\n{monster_spawner.get_region_monster_info(region_name)}")
                else:
                    print("잘못된 번호입니다.")
            except ValueError:
                print("숫자를 입력해주세요.")
        
        elif choice == "3":
            print("\n어느 지역에서 요괴를 소환하시겠습니까?")
            region_list = list(regions.keys())
            for i, region in enumerate(region_list, 1):
                monsters_count = len(monster_spawner.get_monsters_in_region(region))
                print(f"{i}. {region} (요괴 종류: {monsters_count}종)")
            
            try:
                region_choice = int(input("지역 번호> ")) - 1
                if 0 <= region_choice < len(region_list):
                    region_name = region_list[region_choice]
                    monster = monster_spawner.get_random_monster(region_name)
                    
                    print(f"\n👹 {monster.name}이(가) 나타났다!")
                    print(f"설명: {getattr(monster, 'description', '알 수 없는 요괴')}")
                    print(f"HP: {monster.max_hp}, 공격: {monster.attack}, 방어: {monster.defence}")
                    print(f"속도: {monster.speed}, 경험치: {monster.exp_reward}")
                    
                    if hasattr(monster, 'special_traits'):
                        print(f"특징: {monster.special_traits.get('trait_type', '일반')}")
                    
                    if monster.status_chance:
                        status_list = list(monster.status_chance.keys())
                        print(f"상태이상: {', '.join(status_list)}")
                
                else:
                    print("잘못된 번호입니다.")
            except ValueError:
                print("숫자를 입력해주세요.")
        
        elif choice == "4":
            print("\n요괴 목록:")
            monster_list = list(monster_data.keys())
            for i, monster_name in enumerate(monster_list, 1):
                print(f"{i}. {monster_name}")
            
            try:
                monster_choice = int(input("요괴 번호> ")) - 1
                if 0 <= monster_choice < len(monster_list):
                    monster_name = monster_list[monster_choice]
                    data = monster_data[monster_name]
                    
                    print(f"\n=== {monster_name} ===")
                    print(f"설명: {data['description']}")
                    print(f"체력: {data['hp']}")
                    print(f"공격력: {data['attack']}")
                    print(f"방어력: {data['defence']}")
                    print(f"속도: {data['speed']}")
                    print(f"경험치: {data['exp_reward']}")
                    print(f"특수기: {data['skill']}")
                    print(f"출현지역: {', '.join(data['regions'])}")
                    print(f"특징: {data['special_traits']['trait_type']}")
                    
                    # 특수 능력 설명
                    traits = data['special_traits']
                    if traits.get('escape_chance'):
                        print(f"- 도망 확률: {int(traits['escape_chance'] * 100)}%")
                    if traits.get('evasion_bonus'):
                        print(f"- 회피 보너스: +{int(traits['evasion_bonus'] * 100)}%")
                    if traits.get('pack_spawn'):
                        print(f"- 무리 출현 확률: {int(traits.get('pack_chance', 0) * 100)}%")
                    if traits.get('sp_damage'):
                        print(f"- 정신력 피해: -{traits['sp_damage']}")
                
                else:
                    print("잘못된 번호입니다.")
            except ValueError:
                print("숫자를 입력해주세요.")
        
        elif choice == "5":
            print("\n=== 지역별 요괴 출몰 현황 ===")
            for region_name in regions.keys():
                monsters = monster_spawner.get_monsters_in_region(region_name)
                if monsters:
                    danger_levels = []
                    for monster_name in monsters:
                        data = monster_data[monster_name]
                        danger = monster_spawner._get_danger_level(data)
                        danger_levels.append(danger)
                    
                    most_dangerous = max(danger_levels, key=['약함', '보통', '위험', '매우위험'].index)
                    print(f"📍 {region_name}: {len(monsters)}종 (최고위험도: {most_dangerous})")
                    print(f"   출몰 요괴: {', '.join(monsters)}")
                else:
                    print(f"📍 {region_name}: 특별한 요괴 없음")
        
        elif choice == "6":
            print("요괴 시스템 테스트를 종료합니다.")
            break
        
        else:
            print("잘못된 선택입니다.")

if __name__ == "__main__":
    main() 