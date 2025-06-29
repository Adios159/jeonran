"""
지역 시스템 테스트 프로그램
"""
from systems.region import region_manager, regions

def main():
    print("🗺️ 조선시대 지역 시스템 테스트")
    print("=" * 50)
    
    while True:
        print(f"\n현재 위치: {region_manager.current_region}")
        print(region_manager.get_region_info())
        
        print("\n=== 메뉴 ===")
        print("1. 지역 이동")
        print("2. 모든 지역 보기")
        print("3. 현재 지역 상세 정보")
        print("4. 종료")
        
        choice = input("\n선택> ")
        
        if choice == "1":
            destinations = region_manager.get_available_destinations()
            if not destinations:
                print("이동 가능한 지역이 없습니다.")
                continue
            
            print("\n이동 가능한 지역:")
            for i, dest in enumerate(destinations, 1):
                danger = regions[dest]["features"].get("위험도", "안전")
                print(f"{i}. {dest} (위험도: {danger})")
            
            print("0. 취소")
            
            try:
                dest_choice = int(input("이동할 지역 번호> "))
                if dest_choice == 0:
                    continue
                elif 1 <= dest_choice <= len(destinations):
                    destination = destinations[dest_choice - 1]
                    success, message = region_manager.travel_to(destination)
                    print(f"\n{message}")
                else:
                    print("잘못된 번호입니다.")
            except ValueError:
                print("숫자를 입력해주세요.")
        
        elif choice == "2":
            region_manager.list_all_regions()
        
        elif choice == "3":
            current_data = region_manager.get_current_region_data()
            print(f"\n=== {current_data['name']} 상세 정보 ===")
            print(f"설명: {current_data['description']}")
            print(f"인접 지역: {', '.join(current_data['adjacent_regions'])}")
            print("특수 기능:")
            for feature, value in current_data['features'].items():
                if value is True:
                    print(f"  ✓ {feature}")
                elif value is False:
                    print(f"  ✗ {feature}")
                else:
                    print(f"  • {feature}: {value}")
        
        elif choice == "4":
            print("지역 시스템 테스트를 종료합니다.")
            break
        
        else:
            print("잘못된 선택입니다.")

if __name__ == "__main__":
    main() 