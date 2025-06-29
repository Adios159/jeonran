"""
조선시대 설화 기반 RPG - 지역 시스템
각 지역은 고유한 특성, 연결된 지역, 특수 기능을 가집니다.
"""

# 지역 정보 딕셔너리
regions = {
    "한양": {
        "name": "한양",
        "description": "조선의 중심지이자 왕이 거주하는 도성. 크고 작은 상점들이 즐비하며, 관리들과 상인들로 북적거린다. 플레이어의 기본 거점 역할을 한다.",
        "adjacent_regions": ["제물포", "아우내", "소머리골"],
        "features": {
            "거점": True,
            "상점": True,
            "무기상점": True,
            "약초상점": True,
            "여관": True,
            "안전지역": True,
            "저장소": True
        }
    },

    "제물포": {
        "name": "제물포",
        "description": "서해안의 대표적인 항구 도시. 바닷바람이 차갑고, 어부들과 상인들이 분주히 오간다. 물귀신과 바다 요괴들의 출몰이 잦아 주의가 필요하다.",
        "adjacent_regions": ["한양", "탐라국"],
        "features": {
            "항구": True,
            "상점": True,
            "약초상점": True,
            "배편": ["탐라국"],
            "수산물상점": True,
            "물귀신_출몰": True
        }
    },

    "한밭": {
        "name": "한밭",
        "description": "내륙 깊숙한 곳에 위치한 중심지. 넓은 평야와 작은 마을들이 점재해 있으나, 최근 요괴들의 출현이 잦아 상인들의 발길이 끊어졌다.",
        "adjacent_regions": ["아우내", "빛고을"],
        "features": {
            "전투지역": True,
            "높은_요괴출현율": True,
            "상점": False,
            "경험치_보너스": 1.2,
            "위험도": "높음"
        }
    },

    "아우내": {
        "name": "아우내", 
        "description": "남북을 잇는 교통의 요충지. 각지에서 온 행상들과 여행자들이 쉬어가는 곳이다. 비교적 안전하지만 때로는 도적들이 출몰하기도 한다.",
        "adjacent_regions": ["한양", "한밭"],
        "features": {
            "교통중심지": True,
            "여관": True,
            "이동비용_할인": 0.8,
            "정보상": True,
            "도적_출몰": True,
            "위험도": "낮음"
        }
    },

    "빛고을": {
        "name": "빛고을",
        "description": "남부 지방의 문화 중심지. 따뜻한 기후 덕분에 다양한 약초와 특산물이 풍부하다. 학자들과 의원들이 모여들어 번성하고 있다.",
        "adjacent_regions": ["한밭", "가마뫼"],
        "features": {
            "상점": True,
            "약초상점": True,
            "대형약초상점": True,
            "의원": True,
            "학자": True,
            "약초_할인": 0.7,
            "치료비_할인": 0.8,
            "문화중심지": True
        }
    },

    "가마뫼": {
        "name": "가마뫼",
        "description": "남동쪽 해안가의 작은 도시. 화산 지형으로 인해 화속성 요괴들이 자주 나타난다. 바다를 통해 먼 탐라국과 연결되는 중요한 항구다.",
        "adjacent_regions": ["빛고을", "탐라국"],
        "features": {
            "항구": True,
            "상점": True,
            "약초상점": True,
            "화산지형": True,
            "화속성_요괴출몰": True,
            "배편": ["탐라국"],
            "온천": True,
            "MP회복_보너스": 1.5
        }
    },

    "소머리골": {
        "name": "소머리골",
        "description": "한양 북쪽의 깊은 산골짜기. 음침하고 으스스한 기운이 감돌며, 정신을 혼미하게 만드는 요괴들이 서식한다. 함부로 들어가서는 안 되는 곳이다.",
        "adjacent_regions": ["한양"],
        "features": {
            "정신력_페널티": -10,
            "상점": False,
            "정신계_요괴출몰": True,
            "높은_요괴출현율": True,
            "위험도": "매우높음",
            "경험치_보너스": 1.5,
            "저주_확률": 0.3,
            "고립지역": True
        }
    },

    "탐라국": {
        "name": "탐라국",
        "description": "먼 바다의 신비로운 섬나라. 독특한 문화와 희귀한 요괴들이 존재한다. 육지에서는 배를 타고만 갈 수 있으며, 모험가들 사이에서는 전설의 땅으로 불린다.",
        "adjacent_regions": ["제물포", "가마뫼"],
        "features": {
            "섬지역": True,
            "배편_필수": True,
            "희귀_요괴출몰": True,
            "희귀_이벤트": True,
            "특산품상점": True,
            "경험치_보너스": 2.0,
            "위험도": "극도로높음",
            "전설의_땅": True
        }
    }
}

# 지역 관리 클래스
class RegionManager:
    def __init__(self):
        self.current_region = "한양"  # 기본 시작 지역

    def get_current_region_data(self):
        """현재 지역 정보 반환"""
        return regions[self.current_region]

    def get_region_data(self, region_name):
        """특정 지역 정보 반환"""
        return regions.get(region_name)

    def can_travel_to(self, destination):
        """현재 지역에서 목적지로 이동 가능한지 확인"""
        current = self.get_current_region_data()
        
        # 목적지가 인접 지역에 있는지 확인
        if destination not in current["adjacent_regions"]:
            return False
        
        # 배편이 필요한 지역인지 확인
        dest_data = regions.get(destination)
        if dest_data and dest_data["features"].get("배편_필수"):
            # 현재 지역에 항구가 있고, 배편 목록에 목적지가 있는지 확인
            if current["features"].get("항구"):
                available_ships = current["features"].get("배편", [])
                return destination in available_ships
            return False
        
        return True

    def travel_to(self, destination):
        """지역 이동"""
        if not self.can_travel_to(destination):
            return False, f"{destination}로 이동할 수 없습니다."
        
        old_region = self.current_region
        self.current_region = destination
        
        # 이동 시 특수 효과 적용
        new_region_data = self.get_current_region_data()
        messages = [f"{old_region}에서 {destination}로 이동했습니다."]
        
        if new_region_data["features"].get("정신력_페널티"):
            penalty = new_region_data["features"]["정신력_페널티"]
            messages.append(f"이곳의 음산한 기운으로 정신력이 {abs(penalty)} 감소했습니다.")
        
        return True, "\n".join(messages)

    def get_available_destinations(self):
        """현재 지역에서 이동 가능한 지역 목록 반환"""
        current = self.get_current_region_data()
        destinations = []
        
        for dest in current["adjacent_regions"]:
            if self.can_travel_to(dest):
                destinations.append(dest)
        
        return destinations

    def get_region_info(self, region_name=None):
        """지역 정보 출력"""
        if region_name is None:
            region_name = self.current_region
        
        region_data = self.get_region_data(region_name)
        if not region_data:
            return f"'{region_name}' 지역을 찾을 수 없습니다."
        
        info = [
            f"=== {region_data['name']} ===",
            region_data['description'],
            ""
        ]
        
        features = region_data['features']
        
        # 특수 기능 표시
        if features.get("상점"):
            info.append("🏪 상점이 있습니다.")
        if features.get("약초상점"):
            info.append("🌿 약초상점이 있습니다.")
        if features.get("항구"):
            info.append("⚓ 항구가 있습니다.")
        if features.get("거점"):
            info.append("🏰 안전한 거점입니다.")
        if features.get("위험도"):
            danger = features["위험도"]
            info.append(f"⚠️ 위험도: {danger}")
        
        # 인접 지역
        if region_data["adjacent_regions"]:
            info.append(f"\n📍 연결된 지역: {', '.join(region_data['adjacent_regions'])}")
        
        return "\n".join(info)

    def list_all_regions(self):
        """모든 지역 목록 출력"""
        print("=== 조선 팔도 지역 ===")
        for i, (region_name, region_data) in enumerate(regions.items(), 1):
            current_mark = " (현재 위치)" if region_name == self.current_region else ""
            print(f"{i}. {region_name}{current_mark}")
            print(f"   {region_data['description'][:50]}...")
            if region_data['features'].get('위험도'):
                print(f"   위험도: {region_data['features']['위험도']}")
            print()

    def interact_with_npcs(self):
        """현재 지역의 NPC들과 상호작용할 수 있는 메뉴를 제공합니다."""
        from systems.npc_system import NPCSystem
        
        npc_system = NPCSystem()
        npcs = npc_system.get_npcs_in_region(self.current_region)
        
        if not npcs:
            print(f"📭 {self.current_region}에는 만날 수 있는 사람이 없습니다.")
            return
        
        print(f"\n🏘️ **{self.current_region}의 사람들**")
        print("=" * 40)
        
        for i, npc in enumerate(npcs, 1):
            shop_indicator = " 🏪" if npc.has_shop() else ""
            print(f"{i}. {npc.name}{shop_indicator}")
        print(f"{len(npcs) + 1}. 돌아가기")
        print("=" * 40)
        
        while True:
            try:
                choice = input(f"\n만나고 싶은 사람을 선택하세요 (1-{len(npcs) + 1}): ").strip()
                
                if choice == str(len(npcs) + 1):
                    break
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(npcs):
                    selected_npc = npcs[choice_num - 1]
                    print(npc_system.interact_with_npc(selected_npc))
                    
                    # 상점이 있는 경우 상점 이용 옵션 제공
                    if selected_npc.has_shop():
                        shop_choice = input("\n상점을 이용하시겠습니까? (y/n): ").strip().lower()
                        if shop_choice == 'y':
                            print("🚧 상점 시스템은 아직 구현되지 않았습니다.")
                    
                    input("\n계속하려면 Enter를 누르세요...")
                else:
                    print(f"⚠️ 1부터 {len(npcs) + 1} 사이의 숫자를 입력하세요.")
                    
            except ValueError:
                print("⚠️ 올바른 숫자를 입력하세요.")
            except KeyboardInterrupt:
                print("\n👋 대화를 마칩니다.")
                break

# 전역 지역 관리자 인스턴스
region_manager = RegionManager() 