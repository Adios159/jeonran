"""
최적화된 인벤토리 시스템
용량 계산 캐시, 배치 작업, 이벤트 시스템
"""
from typing import Dict, List, Optional, Callable


class OptimizedInventory:
    """최적화된 인벤토리 클래스"""
    
    def __init__(self, max_capacity: int = 30):
        self.items: Dict[str, int] = {}
        self.weapons: List[str] = []
        self.max_capacity = max_capacity
        
        # 캐시된 용량 정보
        self._cached_used_capacity = 0
        self._cache_dirty = True
        
        # 이벤트 콜백
        self._on_change_callbacks: List[Callable] = []
        
        # 성능 통계
        self._stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'operations': 0
        }
    
    def _invalidate_cache(self):
        """캐시 무효화"""
        self._cache_dirty = True
    
    def _update_cache(self):
        """용량 캐시 업데이트"""
        if not self._cache_dirty:
            self._stats['cache_hits'] += 1
            return
        
        self._stats['cache_misses'] += 1
        item_slots = sum(self.items.values())
        weapon_slots = len(self.weapons)
        self._cached_used_capacity = item_slots + weapon_slots
        self._cache_dirty = False
    
    def _trigger_change_events(self):
        """변경 이벤트 트리거"""
        for callback in self._on_change_callbacks:
            try:
                callback(self)
            except Exception as e:
                print(f"⚠️ 인벤토리 이벤트 오류: {e}")
    
    def add_change_listener(self, callback: Callable):
        """인벤토리 변경 리스너 추가"""
        self._on_change_callbacks.append(callback)
    
    def remove_change_listener(self, callback: Callable):
        """인벤토리 변경 리스너 제거"""
        if callback in self._on_change_callbacks:
            self._on_change_callbacks.remove(callback)
    
    def add_item(self, item_name: str, quantity: int = 1) -> bool:
        """아이템 추가 (최적화된 버전)"""
        self._stats['operations'] += 1
        
        if self.get_available_capacity() < quantity:
            return False
        
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
        
        self._invalidate_cache()
        self._trigger_change_events()
        return True
    
    def add_items_batch(self, items: Dict[str, int]) -> Dict[str, bool]:
        """배치 아이템 추가"""
        results = {}
        total_needed = sum(items.values())
        
        if not self.can_add_item(total_needed):
            return {item: False for item in items}
        
        for item_name, quantity in items.items():
            results[item_name] = self.add_item(item_name, quantity)
        
        return results
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """아이템 제거 (최적화된 버전)"""
        self._stats['operations'] += 1
        
        if item_name not in self.items:
            return False
        
        if self.items[item_name] < quantity:
            return False
        
        self.items[item_name] -= quantity
        if self.items[item_name] == 0:
            del self.items[item_name]
        
        self._invalidate_cache()
        self._trigger_change_events()
        return True
    
    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """아이템 보유 확인"""
        return self.items.get(item_name, 0) >= quantity
    
    def has_items_batch(self, items: Dict[str, int]) -> Dict[str, bool]:
        """배치 아이템 보유 확인"""
        return {item: self.has_item(item, quantity) for item, quantity in items.items()}
    
    def get_item_count(self, item_name: str) -> int:
        """아이템 개수 반환"""
        return self.items.get(item_name, 0)
    
    def get_used_capacity(self) -> int:
        """현재 사용 중인 인벤토리 칸 수 (캐시된 결과)"""
        self._update_cache()
        return self._cached_used_capacity
    
    def get_available_capacity(self) -> int:
        """사용 가능한 인벤토리 칸 수"""
        return self.max_capacity - self.get_used_capacity()
    
    def can_add_item(self, quantity: int = 1) -> bool:
        """아이템 추가 가능 여부"""
        return self.get_available_capacity() >= quantity
    
    def can_add_weapon(self, count: int = 1) -> bool:
        """무기 추가 가능 여부"""
        return self.get_available_capacity() >= count
    
    def add_weapon(self, weapon_id: str) -> bool:
        """무기 추가"""
        self._stats['operations'] += 1
        
        if not self.can_add_weapon():
            return False
        
        self.weapons.append(weapon_id)
        self._invalidate_cache()
        self._trigger_change_events()
        return True
    
    def add_weapons_batch(self, weapon_ids: List[str]) -> List[bool]:
        """배치 무기 추가"""
        if not self.can_add_weapon(len(weapon_ids)):
            return [False] * len(weapon_ids)
        
        results = []
        for weapon_id in weapon_ids:
            results.append(self.add_weapon(weapon_id))
        
        return results
    
    def remove_weapon(self, weapon_id: str) -> bool:
        """무기 제거"""
        self._stats['operations'] += 1
        
        if weapon_id in self.weapons:
            self.weapons.remove(weapon_id)
            self._invalidate_cache()
            self._trigger_change_events()
            return True
        return False
    
    def has_weapon(self, weapon_id: str) -> bool:
        """무기 보유 확인"""
        return weapon_id in self.weapons
    
    def list_weapons(self) -> List[str]:
        """무기 목록 반환"""
        return self.weapons.copy()
    
    def is_empty(self) -> bool:
        """인벤토리 비어있는지 확인"""
        return len(self.items) == 0 and len(self.weapons) == 0
    
    def cleanup_items(self):
        """0개인 아이템 정리"""
        items_to_remove = [name for name, count in self.items.items() if count <= 0]
        if items_to_remove:
            for item_name in items_to_remove:
                del self.items[item_name]
            self._invalidate_cache()
            self._trigger_change_events()
    
    def get_summary(self) -> Dict:
        """인벤토리 요약 정보"""
        return {
            'total_items': len(self.items),
            'total_item_count': sum(self.items.values()),
            'total_weapons': len(self.weapons),
            'used_capacity': self.get_used_capacity(),
            'available_capacity': self.get_available_capacity(),
            'capacity_percentage': (self.get_used_capacity() / self.max_capacity) * 100,
            'is_nearly_full': self.get_used_capacity() >= self.max_capacity * 0.9
        }
    
    def get_performance_stats(self) -> Dict:
        """성능 통계 반환"""
        total_cache_operations = self._stats['cache_hits'] + self._stats['cache_misses']
        hit_rate = (self._stats['cache_hits'] / total_cache_operations * 100) if total_cache_operations > 0 else 0
        
        return {
            'total_operations': self._stats['operations'],
            'cache_hits': self._stats['cache_hits'],
            'cache_misses': self._stats['cache_misses'],
            'cache_hit_rate': f"{hit_rate:.1f}%"
        }
    
    def optimize(self):
        """인벤토리 최적화 (정리 작업)"""
        self.cleanup_items()
        # 추가 최적화 작업...
        print("🔧 인벤토리 최적화 완료")


# 인벤토리 모니터링 함수들
def create_capacity_monitor() -> Callable:
    """용량 모니터링 콜백 생성"""
    def monitor(inventory: OptimizedInventory):
        summary = inventory.get_summary()
        if summary['is_nearly_full']:
            print(f"⚠️ 인벤토리가 {summary['capacity_percentage']:.1f}% 찼습니다!")
    return monitor


def create_stats_logger() -> Callable:
    """통계 로깅 콜백 생성"""
    def logger(inventory: OptimizedInventory):
        stats = inventory.get_performance_stats()
        if stats['total_operations'] % 100 == 0:  # 100회 작업마다 로그
            print(f"📊 인벤토리 성능: {stats['cache_hit_rate']} 캐시 적중률")
    return logger 