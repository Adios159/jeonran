"""
전란 그리고 요괴 - 중앙화된 데이터 관리 시스템
모든 JSON 데이터를 한 번에 로딩하고 캐시하여 성능을 최적화합니다.
"""

import json
import os
from typing import Dict, Any, Optional
import time


class DataManager:
    """중앙화된 데이터 관리 시스템"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._last_modified: Dict[str, float] = {}
        self._initialized = False
        
    def initialize(self):
        """모든 데이터를 한 번에 로딩"""
        if self._initialized:
            return
            
        print("📚 게임 데이터를 로딩하는 중...")
        start_time = time.time()
        
        # JSON 파일들을 병렬로 로딩
        data_files = {
            'items': 'data/items.json',
            'weapons': 'data/weapons.json',
            'shops': 'data/shops.json',
            'npcs': 'data/npcs.json',
            'skills': 'data/skills.json',
            'minions': 'data/minions.json',
            'midbosses': 'data/midbosses.json',
            'quests': 'data/quests.json'
        }
        
        for key, filepath in data_files.items():
            self._load_file(key, filepath)
        
        load_time = time.time() - start_time
        print(f"✅ 데이터 로딩 완료 ({load_time:.3f}초)")
        self._initialized = True
    
    def _load_file(self, key: str, filepath: str) -> Optional[Any]:
        """개별 파일 로딩 및 캐시 관리"""
        if not os.path.exists(filepath):
            print(f"⚠️ 파일을 찾을 수 없습니다: {filepath}")
            return None
            
        try:
            # 파일 수정 시간 확인
            mod_time = os.path.getmtime(filepath)
            
            # 캐시된 데이터가 있고 파일이 수정되지 않았으면 캐시 반환
            if (key in self._cache and 
                key in self._last_modified and 
                self._last_modified[key] >= mod_time):
                return self._cache[key]
            
            # 파일 로딩
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 캐시 업데이트
            self._cache[key] = data
            self._last_modified[key] = mod_time
            
            return data
            
        except Exception as e:
            print(f"❌ 파일 로딩 오류 ({filepath}): {e}")
            return None
    
    def get(self, key: str, refresh: bool = False) -> Optional[Any]:
        """데이터 조회"""
        if not self._initialized:
            self.initialize()
            
        if refresh or key not in self._cache:
            # 파일 경로 매핑
            file_map = {
                'items': 'data/items.json',
                'weapons': 'data/weapons.json',
                'shops': 'data/shops.json',
                'npcs': 'data/npcs.json',
                'skills': 'data/skills.json',
                'minions': 'data/minions.json',
                'midbosses': 'data/midbosses.json',
                'quests': 'data/quests.json'
            }
            
            if key in file_map:
                return self._load_file(key, file_map[key])
        
        return self._cache.get(key)
    
    def clear_cache(self):
        """캐시 초기화"""
        self._cache.clear()
        self._last_modified.clear()
        self._initialized = False
    
    def get_cache_info(self) -> Dict[str, Any]:
        """캐시 정보 반환"""
        return {
            'cached_files': list(self._cache.keys()),
            'cache_size': len(self._cache),
            'initialized': self._initialized,
            'memory_usage': sum(len(str(data)) for data in self._cache.values())
        }


# 전역 인스턴스
data_manager = DataManager()


def get_data(key: str, refresh: bool = False) -> Optional[Any]:
    """편의 함수: 데이터 조회"""
    return data_manager.get(key, refresh)


def initialize_data():
    """편의 함수: 데이터 초기화"""
    data_manager.initialize()


def clear_data_cache():
    """편의 함수: 캐시 초기화"""
    data_manager.clear_cache() 