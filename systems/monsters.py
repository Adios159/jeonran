"""
조선시대 설화 기반 RPG - 몬스터 시스템
각 몬스터는 고유한 능력과 출현 지역을 가집니다.
"""
import random

# 몬스터 데이터베이스
monster_data = {
    "도깨비불": {
        "name": "도깨비불",
        "description": "어두운 밤길에서 혼자 다니는 이를 따라다니며 놀리는 장난스런 불덩이",
        "hp": 30,
        "attack": 8,
        "defence": 0,
        "speed": 12,
        "exp_reward": 25,
        "skill": "화상_부여",
        "regions": ["제물포", "탐라국"],
        "special_traits": {
            "escape_chance": 0.6,
            "trait_type": "escapist"
        },
        "status_chance": {"burn": 0.4}
    },

    "허깨비": {
        "name": "허깨비",
        "description": "환각처럼 나타났다가 사라지는 그림자 같은 존재",
        "hp": 25,
        "attack": 6,
        "defence": 1,
        "speed": 15,
        "exp_reward": 20,
        "skill": "혼란_부여",
        "regions": ["아우내", "소머리골"],
        "special_traits": {
            "evasion_bonus": 0.3,
            "trait_type": "evasive"
        },
        "status_chance": {"freeze": 0.5}
    },

    "들개령": {
        "name": "들개령",
        "description": "굶주린 야생개가 혼을 잃고 요괴화된 모습",
        "hp": 35,
        "attack": 10,
        "defence": 2,
        "speed": 14,
        "exp_reward": 30,
        "skill": "출혈_효과",
        "regions": ["한밭", "아우내"],
        "special_traits": {
            "pack_spawn": True,
            "pack_chance": 0.4,
            "trait_type": "pack_hunter"
        },
        "status_chance": {"poison": 0.3}
    },

    "독꼬리": {
        "name": "독꼬리",
        "description": "꼬리에 맹독을 품은 도마뱀형 요괴",
        "hp": 28,
        "attack": 9,
        "defence": 3,
        "speed": 10,
        "exp_reward": 28,
        "skill": "중독_공격",
        "regions": ["가마뫼", "빛고을"],
        "special_traits": {
            "poison_stacking": True,
            "trait_type": "poisoner"
        },
        "status_chance": {"poison": 0.6}
    },

    "썩은시체": {
        "name": "썩은시체",
        "description": "묘지에서 되살아난 무명자의 시신",
        "hp": 45,
        "attack": 7,
        "defence": 5,
        "speed": 6,
        "exp_reward": 35,
        "skill": "무작위_상태이상",
        "regions": ["소머리골"],
        "special_traits": {
            "random_status": True,
            "slow_but_tough": True,
            "trait_type": "tank"
        },
        "status_chance": {"random": 0.4}
    },

    "흐느낌귀": {
        "name": "흐느낌귀",
        "description": "밤마다 흐느끼는 소리만 들리는 망령",
        "hp": 32,
        "attack": 6,
        "defence": 2,
        "speed": 8,
        "exp_reward": 26,
        "skill": "공포_부여",
        "regions": ["한양", "소머리골"],
        "special_traits": {
            "sp_damage": 5,
            "trait_type": "mental_attacker"
        },
        "status_chance": {"stun": 0.5}
    },

    "그늘망령": {
        "name": "그늘망령",
        "description": "해가 들지 않는 골목에서 자라는 어둠의 정령",
        "hp": 30,
        "attack": 7,
        "defence": 3,
        "speed": 11,
        "exp_reward": 24,
        "skill": "시야_차단",
        "regions": ["한양", "빛고을"],
        "special_traits": {
            "accuracy_debuff": 0.3,
            "evasion_bonus": 0.2,
            "trait_type": "debuffer"
        },
        "status_chance": {"freeze": 0.4}
    },

    "어스름그림자": {
        "name": "어스름그림자",
        "description": "땅거미 질 무렵 출몰하며 기억을 흐리게 함",
        "hp": 27,
        "attack": 6,
        "defence": 1,
        "speed": 13,
        "exp_reward": 22,
        "skill": "기술_봉쇄",
        "regions": ["한양", "탐라국"],
        "special_traits": {
            "skill_seal": True,
            "trait_type": "controller"
        },
        "status_chance": {"stun": 0.5}
    },

    "뒤틀린손": {
        "name": "뒤틀린손",
        "description": "땅속에서 솟아난 손들이 마구잡이로 덮쳐온다",
        "hp": 40,
        "attack": 11,
        "defence": 4,
        "speed": 7,
        "exp_reward": 32,
        "skill": "속박_공격",
        "regions": ["제물포", "가마뫼"],
        "special_traits": {
            "binding_attack": True,
            "trait_type": "controller"
        },
        "status_chance": {"freeze": 0.4}
    },

    "메아리귀": {
        "name": "메아리귀",
        "description": "사방에서 들려오는 자신의 목소리에 미쳐가는 혼령",
        "hp": 26,
        "attack": 5,
        "defence": 2,
        "speed": 9,
        "exp_reward": 23,
        "skill": "정신_혼란",
        "regions": ["소머리골"],
        "special_traits": {
            "mental_combo": True,
            "sp_damage": 3,
            "trait_type": "mental_attacker"
        },
        "status_chance": {"stun": 0.4, "poison": 0.3}
    }
}

class MonsterFactory:
    """몬스터 생성 및 관리"""
    
    @staticmethod
    def create_monster(monster_name):
        """몬스터 데이터를 기반으로 Enemy 인스턴스 생성"""
        if monster_name not in monster_data:
            raise ValueError(f"몬스터 '{monster_name}'를 찾을 수 없습니다.")
        
        # 기존 Enemy 클래스를 import해야 하므로 여기서 import
        from characters.enemy import Enemy
        
        data = monster_data[monster_name]
        
        # Enemy 인스턴스 생성
        monster = Enemy(
            name=data["name"],
            max_hp=data["hp"],
            attack=data["attack"],
            defence=data["defence"],
            speed=data["speed"],
            exp_reward=data["exp_reward"],
            status_chance=data["status_chance"]
        )
        
        # 몬스터 고유 정보 추가
        monster.description = data["description"]
        monster.skill = data["skill"]
        monster.regions = data["regions"]
        monster.special_traits = data["special_traits"]
        monster.trait_type = data["special_traits"].get("trait_type", "normal")
        
        # 특수 능력 적용
        MonsterFactory._apply_special_traits(monster)
        
        return monster
    
    @staticmethod
    def _apply_special_traits(monster):
        """몬스터에 특수 능력 적용"""
        traits = monster.special_traits
        
        # 도망치는 몬스터 (도깨비불)
        if traits.get("escape_chance"):
            original_choose_action = monster.choose_action
            
            def escape_action(target):
                if random.random() < traits["escape_chance"]:
                    print(f"{monster.name}이(가) 빠르게 도망쳤다!")
                    monster.current_hp = 0  # 도망 = 전투 종료
                    return
                original_choose_action(target)
            
            monster.choose_action = escape_action
        
        # 회피 보너스 (허깨비, 그늘망령)
        if traits.get("evasion_bonus"):
            # 향후 회피 시스템 구현 시 사용
            pass
        
        # 무리 스폰 (들개령)
        if traits.get("pack_spawn"):
            # 향후 다중 전투 시스템 구현 시 사용
            pass

class MonsterSpawner:
    """지역별 몬스터 스폰 관리"""
    
    def __init__(self):
        self.region_monsters = self._build_region_monster_map()
    
    def _build_region_monster_map(self):
        """지역별 몬스터 맵 생성"""
        region_map = {}
        
        for monster_name, data in monster_data.items():
            for region in data["regions"]:
                if region not in region_map:
                    region_map[region] = []
                region_map[region].append(monster_name)
        
        return region_map
    
    def get_random_monster(self, region_name):
        """해당 지역에서 랜덤 몬스터 스폰"""
        if region_name not in self.region_monsters:
            # 기본 몬스터 (호롱불) 반환
            from characters.enemy import Enemy
            return Enemy(
                name="호롱불",
                max_hp=50,
                attack=10,
                defence=3,
                speed=5,
                exp_reward=30,
                status_chance={"burn": 0.4}
            )
        
        available_monsters = self.region_monsters[region_name]
        monster_name = random.choice(available_monsters)
        
        # 무리 스폰 체크
        data = monster_data[monster_name]
        if data["special_traits"].get("pack_spawn"):
            pack_chance = data["special_traits"].get("pack_chance", 0)
            if random.random() < pack_chance:
                print(f"여러 마리의 {monster_name}이(가) 무리지어 나타났다!")
        
        return MonsterFactory.create_monster(monster_name)
    
    def get_monsters_in_region(self, region_name):
        """해당 지역의 모든 몬스터 목록 반환"""
        return self.region_monsters.get(region_name, [])
    
    def list_all_monsters(self):
        """모든 몬스터 정보 출력"""
        print("=== 조선 요괴 도감 ===")
        for monster_name, data in monster_data.items():
            print(f"\n👹 {monster_name}")
            print(f"   {data['description']}")
            print(f"   HP: {data['hp']}, 공격: {data['attack']}, 방어: {data['defence']}")
            print(f"   특수기: {data['skill']}")
            print(f"   출현지역: {', '.join(data['regions'])}")
            print(f"   특징: {data['special_traits']['trait_type']}")
    
    def get_region_monster_info(self, region_name):
        """특정 지역의 몬스터 정보 출력"""
        if region_name not in self.region_monsters:
            return f"{region_name}에는 특별한 요괴가 출몰하지 않습니다."
        
        monsters = self.region_monsters[region_name]
        info = [f"=== {region_name} 출몰 요괴 ==="]
        
        for monster_name in monsters:
            data = monster_data[monster_name]
            danger_level = self._get_danger_level(data)
            info.append(f"👹 {monster_name} ({danger_level})")
            info.append(f"   {data['description'][:40]}...")
        
        return "\n".join(info)
    
    def _get_danger_level(self, data):
        """몬스터 위험도 계산"""
        total_stats = data["hp"] + data["attack"] * 2 + data["defence"]
        
        if total_stats >= 60:
            return "매우위험"
        elif total_stats >= 45:
            return "위험"
        elif total_stats >= 30:
            return "보통"
        else:
            return "약함"

# 전역 몬스터 스포너 인스턴스
monster_spawner = MonsterSpawner() 