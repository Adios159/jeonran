"""
조선시대 설화 기반 RPG - 최적화된 몬스터 시스템
JSON 데이터 기반, 메모리 효율적인 몬스터 관리
"""
import random
from typing import List, Dict, Optional, Tuple
from systems.data_manager import get_data


class OptimizedMonsterSpawner:
    """최적화된 몬스터 스포너"""
    
    def __init__(self):
        self._region_cache: Dict[str, List[Dict]] = {}
        self._spawn_weights_cache: Dict[str, List[Tuple[str, float]]] = {}
        self._initialized = False
    
    def _initialize(self):
        """초기화 및 캐시 구축"""
        if self._initialized:
            return
        
        # 데이터 로딩
        minions = get_data('minions') or []
        midbosses = get_data('midbosses') or []
        
        # 모든 몬스터 통합
        all_monsters = minions + midbosses
        
        # 지역별 몬스터 캐시 구축
        for monster in all_monsters:
            regions = monster.get('region', [])
            if isinstance(regions, str):
                regions = [regions]
            
            for region in regions:
                if region not in self._region_cache:
                    self._region_cache[region] = []
                self._region_cache[region].append(monster)
        
        # 지역별 스폰 가중치 캐시 구축
        for region, monsters in self._region_cache.items():
            weights = []
            for monster in monsters:
                spawn_chance = monster.get('spawn_chance', 50) / 100.0
                weights.append((monster['name'], spawn_chance))
            self._spawn_weights_cache[region] = weights
        
        self._initialized = True
    
    def get_random_monsters(self, region_name: str, force_count: Optional[int] = None) -> List:
        """지역에서 랜덤 몬스터 그룹을 생성"""
        self._initialize()
        
        if region_name not in self._region_cache:
            return []
        
        # 스폰 개수 결정
        spawn_count = force_count or self._determine_spawn_count(region_name)
        
        # 몬스터 선택
        selected_monsters = []
        region_monsters = self._region_cache[region_name]
        weights = [monster.get('spawn_chance', 50) for monster in region_monsters]
        
        for _ in range(spawn_count):
            if region_monsters:
                monster_data = random.choices(region_monsters, weights=weights, k=1)[0]
                monster = self._create_monster_from_data(monster_data)
                if monster:
                    selected_monsters.append(monster)
        
        return selected_monsters
    
    def _determine_spawn_count(self, region_name: str) -> int:
        """지역별 위험도에 따른 스폰 개수 결정 (최적화된 버전)"""
        # 지역별 위험도 매핑 (하드코딩 대신 설정 파일로 이동 가능)
        danger_levels = {
            "한양": "안전",
            "제물포": "안전", 
            "아우내": "낮음",
            "빛고을": "안전",
            "한밭": "높음",
            "가마뫼": "높음", 
            "소머리골": "매우높음",
            "탐라국": "극도로높음"
        }
        
        danger = danger_levels.get(region_name, "안전")
        
        # 확률 분포 (미리 계산된 테이블)
        spawn_probabilities = {
            "안전": [(1, 0.85), (2, 0.15)],
            "낮음": [(1, 0.80), (2, 0.20)], 
            "높음": [(1, 0.70), (2, 0.30)],
            "매우높음": [(1, 0.50), (2, 0.40), (3, 0.10)],
            "극도로높음": [(1, 0.30), (2, 0.50), (3, 0.20)]
        }
        
        probs = spawn_probabilities.get(danger, [(1, 1.0)])
        counts, weights = zip(*probs)
        return random.choices(counts, weights=weights)[0]
    
    def _create_monster_from_data(self, monster_data: Dict):
        """몬스터 데이터로부터 Enemy 인스턴스 생성 (지연 임포트)"""
        try:
            from characters.enemy import Enemy
            
            # 기본값 설정
            name = monster_data.get('name', '알 수 없는 요괴')
            hp = monster_data.get('hp', 50)
            attack = monster_data.get('attack', 10)
            defense = monster_data.get('defense', 5)
            speed = monster_data.get('speed', 10)
            
            # 경험치 보상 추출
            exp_reward = monster_data.get('rewards', {}).get('exp', 20)
            
            # Enemy 인스턴스 생성
            monster = Enemy(
                name=name,
                max_hp=hp,
                attack=attack,
                defence=defense,
                speed=speed,
                exp_reward=exp_reward
            )
            
            # 추가 속성 설정
            monster.description = monster_data.get('description', '')
            
            return monster
            
        except ImportError:
            print("❌ Enemy 클래스를 불러올 수 없습니다.")
            return None
    
    def get_monsters_in_region(self, region_name: str) -> List[str]:
        """지역의 몬스터 목록 반환"""
        self._initialize()
        return [monster['name'] for monster in self._region_cache.get(region_name, [])]
    
    def get_region_monster_info(self, region_name: str) -> Dict:
        """지역의 몬스터 정보 요약"""
        self._initialize()
        
        if region_name not in self._region_cache:
            return {"region": region_name, "monsters": [], "total_count": 0}
        
        monsters = self._region_cache[region_name]
        return {
            "region": region_name,
            "monsters": [monster['name'] for monster in monsters],
            "total_count": len(monsters),
            "avg_spawn_chance": sum(m.get('spawn_chance', 50) for m in monsters) / len(monsters)
        }
    
    def clear_cache(self):
        """캐시 초기화"""
        self._region_cache.clear()
        self._spawn_weights_cache.clear()
        self._initialized = False


# 전역 인스턴스
optimized_monster_spawner = OptimizedMonsterSpawner()


# 편의 함수들
def get_random_monsters(region_name: str, force_count: Optional[int] = None) -> List:
    """편의 함수: 랜덤 몬스터 그룹 생성"""
    return optimized_monster_spawner.get_random_monsters(region_name, force_count)


def get_monsters_in_region(region_name: str) -> List[str]:
    """편의 함수: 지역 몬스터 목록"""
    return optimized_monster_spawner.get_monsters_in_region(region_name)


def get_region_monster_info(region_name: str) -> Dict:
    """편의 함수: 지역 몬스터 정보"""
    return optimized_monster_spawner.get_region_monster_info(region_name) 