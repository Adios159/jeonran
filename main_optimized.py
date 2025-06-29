"""
최적화된 메인 게임 루프
- 중앙화된 데이터 관리
- 게임 상태 캐싱
- 비동기 작업 지원
"""
from characters.player import Player
from characters.enemy import Enemy
from systems.battle import start_battle
from systems.data_manager import initialize_data
from systems.monsters_optimized import get_random_monsters
from systems.region import region_manager
from typing import Optional, Dict, Any
import time


class GameStateManager:
    """게임 상태 관리자"""
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.current_menu = "main"
        self.last_action_time = time.time()
        self.performance_stats: Dict[str, Any] = {
            'menu_loads': 0,
            'battles_fought': 0,
            'regions_visited': 0,
            'total_playtime': 0.0
        }
        
        # 캐시된 메뉴 옵션
        self._menu_cache = {}
        self._region_cache = {}
    
    def start_game(self):
        """게임 시작 및 초기화"""
        print("🌕 전란 그리고 요괴 🌕")
        print("게임을 초기화하는 중...")
        
        # 데이터 초기화 (한 번만 실행)
        initialize_data()
        
        # 메인 메뉴
        self.show_main_menu()
    
    def show_main_menu(self):
        """최적화된 메인 메뉴"""
        while True:
            print("\n" + "="*50)
            print("🌕 전란 그리고 요괴 🌕")
            print("="*50)
            
            options = [
                "1. 새 게임 시작",
                "2. 게임 불러오기", 
                "3. 게임 설정",
                "4. 성능 통계 보기",
                "5. 게임 종료"
            ]
            
            for option in options:
                print(option)
            
            choice = input("\n선택> ").strip()
            
            if choice == "1":
                self.start_new_game()
                break
            elif choice == "2":
                if self.load_game():
                    break
            elif choice == "3":
                self.show_settings()
            elif choice == "4":
                self.show_performance_stats()
            elif choice == "5":
                print("게임을 종료합니다.")
                return
            else:
                print("올바른 번호를 입력해주세요.")
    
    def start_new_game(self):
        """새 게임 시작"""
        print("\n=== 새 게임 시작 ===")
        
        # 캐릭터 생성
        name = input("캐릭터 이름을 입력하세요: ").strip()
        if not name:
            name = "무명"
        
        print("\n직업을 선택하세요:")
        jobs = ["무사", "도사", "유랑객"]
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job}")
        
        while True:
            try:
                job_choice = int(input("선택> "))
                if 1 <= job_choice <= len(jobs):
                    selected_job = jobs[job_choice - 1]
                    break
                else:
                    print("올바른 번호를 입력해주세요.")
            except ValueError:
                print("숫자를 입력해주세요.")
        
        # 플레이어 생성
        self.player = Player(name, selected_job)
        self.player.give_starting_items()
        
        print(f"\n{name} ({selected_job})으로 모험을 시작합니다!")
        time.sleep(1)
        
        # 게임 루프 시작
        self.main_game_loop()
    
    def main_game_loop(self):
        """최적화된 메인 게임 루프"""
        if self.player is None:
            print("❌ 플레이어가 초기화되지 않았습니다.")
            return
            
        start_time = time.time()
        
        while self.player.is_alive():
            try:
                self.display_optimized_menu()
                choice = input("\n선택> ").strip()
                
                # 성능 통계 업데이트
                self.performance_stats['menu_loads'] += 1
                self.last_action_time = time.time()
                
                if choice == "1":
                    if self.explore_region_optimized():
                        self.performance_stats['battles_fought'] += 1
                elif choice == "2":
                    if self.travel_menu_optimized():
                        self.performance_stats['regions_visited'] += 1
                elif choice == "3":
                    self.npc_interaction_menu()
                elif choice == "4":
                    self.equipment_menu()
                elif choice == "5":
                    self.show_player_status_optimized()
                elif choice == "6":
                    self.show_region_info_optimized()
                elif choice == "7":
                    self.show_monster_catalog()
                elif choice == "8":
                    self.rest_at_location()
                elif choice == "9":
                    self.game_exit_menu()
                    break
                else:
                    print("올바른 번호를 입력해주세요.")
                    
            except KeyboardInterrupt:
                print("\n\n게임을 중단하시겠습니까? (y/n)")
                if input().lower() in ['y', 'yes', '예']:
                    break
            except Exception as e:
                print(f"❌ 게임 오류: {e}")
                print("게임을 계속 진행합니다...")
        
        # 총 플레이 시간 계산
        self.performance_stats['total_playtime'] = time.time() - start_time
        
        if not self.player.is_alive():
            print("\n💀 게임 오버...")
            self.show_game_over_screen()
    
    def display_optimized_menu(self):
        """캐시된 메뉴 출력"""
        if self.player is None:
            menu_key = f"{region_manager.current_region}_0"
        else:
            menu_key = f"{region_manager.current_region}_{self.player.level}"
        
        if menu_key not in self._menu_cache:
            self._menu_cache[menu_key] = self._generate_menu_content()
        
        print(self._menu_cache[menu_key])
    
    def _generate_menu_content(self):
        """메뉴 콘텐츠 생성"""
        content = [
            "\n" + "="*50,
            "🌕 전란 그리고 요괴 🌕",
            "="*50,
            "1. 지역 탐험 (요괴와 전투)",
            "2. 지역 이동",
            "3. 사람들과 대화",
            "4. 장비 관리",
            "5. 현재 상태 확인",
            "6. 지역 정보 보기",
            "7. 요괴 도감",
            "8. 휴식 (HP/MP 회복)",
            "9. 게임 종료",
            "="*50
        ]
        return "\n".join(content)
    
    def explore_region_optimized(self):
        """최적화된 지역 탐험"""
        if self.player is None:
            print("플레이어가 초기화되지 않았습니다.")
            return False
            
        current_region = region_manager.current_region
        print(f"\n{current_region}을(를) 탐험합니다...")
        
        # 지역 정보 캐싱
        region_key = current_region
        if region_key not in self._region_cache:
            self._region_cache[region_key] = region_manager.get_current_region_data()
        
        region_data = self._region_cache[region_key]
        print(region_data['description'])
        
        # 최적화된 몬스터 스폰
        enemies = get_random_monsters(current_region)
        if not enemies:
            print("이곳은 평화로워 보입니다...")
            return False
        
        # 전투 시작
        battle_result = start_battle(self.player, enemies)
        
        if battle_result == "player_victory":
            # 경험치 계산
            total_base_exp = sum(enemy.exp_reward for enemy in enemies)
            exp_bonus = region_data["features"].get("경험치_보너스", 1.0)
            final_exp = int(total_base_exp * exp_bonus)
            
            if exp_bonus > 1.0:
                print(f"\n🌟 {current_region}의 특별한 기운으로 경험치가 {int((exp_bonus-1)*100)}% 추가!")
            
            self.player.gain_exp(final_exp)
            return True
        elif battle_result == "player_escaped":
            print("\n도망에 성공했습니다!")
            return False
        else:
            return False
    
    def show_performance_stats(self):
        """성능 통계 표시"""
        print("\n📊 **게임 성능 통계**")
        print("=" * 30)
        
        stats = self.performance_stats
        print(f"메뉴 로드 횟수: {stats['menu_loads']}")
        print(f"전투 횟수: {stats['battles_fought']}")
        print(f"방문한 지역 수: {stats['regions_visited']}")
        
        if stats['total_playtime'] > 0:
            hours = int(stats['total_playtime'] // 3600)
            minutes = int((stats['total_playtime'] % 3600) // 60)
            print(f"총 플레이 시간: {hours}시간 {minutes}분")
        
        # 캐시 통계
        print(f"메뉴 캐시 크기: {len(self._menu_cache)}")
        print(f"지역 캐시 크기: {len(self._region_cache)}")
    
    def clear_caches(self):
        """캐시 초기화"""
        self._menu_cache.clear()
        self._region_cache.clear()
        print("🔄 캐시가 초기화되었습니다.")
    
    def load_game(self) -> bool:
        """게임 불러오기"""
        try:
            from systems.save_system import SaveSystem
            save_system = SaveSystem()
            loaded_player = save_system.load_game()
            if loaded_player:
                self.player = loaded_player
                print("게임을 성공적으로 불러왔습니다!")
                return True
            else:
                print("저장된 게임이 없습니다.")
                return False
        except Exception as e:
            print(f"게임을 불러오는 중 오류가 발생했습니다: {e}")
            return False
    
    def show_settings(self):
        """게임 설정"""
        while True:
            print("\n⚙️ 게임 설정")
            print("=" * 30)
            print("1. 캐시 초기화")
            print("2. 성능 통계 초기화")
            print("3. 돌아가기")
            
            choice = input("\n선택> ").strip()
            
            if choice == "1":
                self.clear_caches()
            elif choice == "2":
                self.performance_stats = {
                    'menu_loads': 0,
                    'battles_fought': 0,
                    'regions_visited': 0,
                    'total_playtime': 0.0
                }
                print("🔄 성능 통계가 초기화되었습니다.")
            elif choice == "3":
                break
            else:
                print("올바른 번호를 입력해주세요.")
    
    def travel_menu_optimized(self) -> bool:
        """최적화된 지역 이동 메뉴"""
        if self.player is None:
            return False
            
        try:
            from systems.region import handle_region_travel
            return handle_region_travel(self.player)
        except Exception as e:
            print(f"지역 이동 중 오류가 발생했습니다: {e}")
            return False
    
    def npc_interaction_menu(self):
        """NPC 상호작용 메뉴"""
        if self.player is None:
            return
            
        try:
            from systems.npc_system import handle_npc_interaction
            handle_npc_interaction(self.player)
        except Exception as e:
            print(f"NPC 상호작용 중 오류가 발생했습니다: {e}")
    
    def equipment_menu(self):
        """장비 관리 메뉴"""
        if self.player is None:
            return
            
        try:
            from systems.weapon_system import equipment_management_menu
            equipment_management_menu(self.player)
        except Exception as e:
            print(f"장비 관리 중 오류가 발생했습니다: {e}")
    
    def show_player_status_optimized(self):
        """최적화된 플레이어 상태 표시"""
        if self.player is None:
            return
            
        print("\n" + "="*50)
        print(f"👤 {self.player.name} ({self.player.job}) - Lv.{self.player.level}")
        print("="*50)
        print(f"⚡ HP: {self.player.hp}/{self.player.max_hp}")
        print(f"🔮 MP: {self.player.mp}/{self.player.max_mp}")
        print(f"🗡️  공격력: {self.player.get_effective_attack()}")
        print(f"🛡️  방어력: {self.player.defense}")
        print(f"⚡ 속도: {self.player.speed}")
        print(f"💰 소지금: {self.player.gold}전")
        print(f"📍 현재 위치: {region_manager.current_region}")
        
        # 경험치 표시
        if hasattr(self.player, 'show_exp_progress'):
            self.player.show_exp_progress()
            
        input("\n계속하려면 엔터를 누르세요...")
    
    def show_region_info_optimized(self):
        """최적화된 지역 정보 표시"""
        try:
            from systems.region import show_region_detailed_info
            show_region_detailed_info()
        except Exception as e:
            print(f"지역 정보 표시 중 오류가 발생했습니다: {e}")
    
    def show_monster_catalog(self):
        """요괴 도감 표시"""
        try:
            from systems.monsters_optimized import show_monster_catalog
            show_monster_catalog()
        except Exception as e:
            print(f"요괴 도감 표시 중 오류가 발생했습니다: {e}")
    
    def rest_at_location(self):
        """휴식 기능"""
        if self.player is None:
            return
            
        print("\n🛌 휴식을 취합니다...")
        
        # 지역별 특별 회복 보너스 확인
        region_data = region_manager.get_current_region_data()
        healing_bonus = region_data.get("features", {}).get("회복_보너스", 1.0)
        
        # 기본 회복량
        hp_recovery = min(20, self.player.max_hp - self.player.hp)
        mp_recovery = min(10, self.player.max_mp - self.player.mp)
        
        # 보너스 적용
        if healing_bonus > 1.0:
            hp_recovery = int(hp_recovery * healing_bonus)
            mp_recovery = int(mp_recovery * healing_bonus)
            print(f"✨ {region_manager.current_region}의 특별한 기운으로 회복량이 증가!")
        
        self.player.hp = min(self.player.max_hp, self.player.hp + hp_recovery)
        self.player.mp = min(self.player.max_mp, self.player.mp + mp_recovery)
        
        print(f"❤️ HP +{hp_recovery} 회복")
        print(f"💙 MP +{mp_recovery} 회복")
        print("기분이 상쾌해졌습니다!")
        
        input("\n계속하려면 엔터를 누르세요...")
    
    def game_exit_menu(self):
        """게임 종료 메뉴"""
        if self.player is None:
            return
            
        while True:
            print("\n💾 게임 종료")
            print("=" * 30)
            print("1. 저장 후 종료")
            print("2. 저장하지 않고 종료")
            print("3. 돌아가기")
            
            choice = input("\n선택> ").strip()
            
            if choice == "1":
                try:
                    from systems.save_system import SaveSystem
                    save_system = SaveSystem()
                    if save_system.save_game(self.player):
                        print("게임이 저장되었습니다. 안녕히 가세요!")
                        exit()
                    else:
                        print("저장에 실패했습니다.")
                except Exception as e:
                    print(f"저장 중 오류가 발생했습니다: {e}")
            elif choice == "2":
                print("저장하지 않고 게임을 종료합니다. 안녕히 가세요!")
                exit()
            elif choice == "3":
                break
            else:
                print("올바른 번호를 입력해주세요.")
    
    def show_game_over_screen(self):
        """게임 오버 화면"""
        print("\n" + "="*50)
        print("💀 게임 오버 💀")
        print("="*50)
        
        if self.player:
            print(f"전사한 영웅: {self.player.name} ({self.player.job})")
            print(f"도달한 레벨: {self.player.level}")
            print(f"최종 위치: {region_manager.current_region}")
        
        print("\n당신의 모험이 여기서 끝났습니다...")
        print("다시 도전하시겠습니까?")
        
        choice = input("\n다시 시작하시겠습니까? (y/n): ").strip().lower()
        if choice in ['y', 'yes', '예']:
            self.player = None
            self.clear_caches()
            self.show_main_menu()


def main():
    """최적화된 메인 함수"""
    game_manager = GameStateManager()
    game_manager.start_game()


if __name__ == "__main__":
    main() 