import math


class ExperienceSystem:
    """
    조선시대 RPG 경험치 및 레벨링 시스템
    
    레벨 구간별 성장률:
    - 1~49레벨: 빠른 지수 증가 (초보자 친화적)
    - 50~99레벨: 완만한 지수 증가 (중급자)
    - 100~150레벨: 로그 증가 (고급자, 엔드게임)
    """
    
    # 기본 설정값
    BASE_EXP = 80           # 레벨 1에서 2로 가는 기본 경험치
    GROWTH1 = 1.18          # Lv 1~49 성장률 (조금 완만하게 조정)
    GROWTH2 = 1.015         # Lv 50~99 완만 지수 성장률
    K = 2200                # Lv 100~150 로그 증가 계수
    MAX_LEVEL = 150         # 최대 레벨
    
    def __init__(self):
        # 미리 계산해두는 기준점 (성능 최적화)
        self.exp_49 = int(self.BASE_EXP * (self.GROWTH1 ** (49 - 1)))
        self.exp_99 = int(self.exp_49 * (self.GROWTH2 ** (99 - 49)))
        
        # 레벨별 누적 경험치 캐시 (자주 사용되므로 미리 계산)
        self._total_exp_cache = {}
        self._precompute_total_exp()
    
    def _precompute_total_exp(self):
        """레벨별 총 누적 경험치를 미리 계산하여 캐시에 저장"""
        total = 0
        for level in range(1, self.MAX_LEVEL + 1):
            if level > 1:
                total += self.exp_needed_for_level(level)
            self._total_exp_cache[level] = total
    
    def exp_needed_for_level(self, level: int) -> int:
        """
        특정 레벨에 도달하기 위해 필요한 경험치
        (이전 레벨에서 해당 레벨로 가는 데 필요한 경험치)
        
        Args:
            level: 목표 레벨 (2~150)
            
        Returns:
            int: 필요한 경험치
        """
        if level < 2:
            return 0
        elif level <= 50:
            return int(self.BASE_EXP * (self.GROWTH1 ** (level - 2)))
        elif level <= 100:
            return int(self.exp_49 * (self.GROWTH2 ** (level - 50)))
        elif level <= self.MAX_LEVEL:
            return int(self.exp_99 + self.K * math.log(level - 99))
        else:
            raise ValueError(f"최대 레벨은 {self.MAX_LEVEL}입니다.")
    
    def total_exp_for_level(self, level: int) -> int:
        """
        특정 레벨에 도달하기 위한 총 누적 경험치
        
        Args:
            level: 목표 레벨 (1~150)
            
        Returns:
            int: 총 누적 경험치
        """
        if level < 1 or level > self.MAX_LEVEL:
            raise ValueError(f"레벨은 1~{self.MAX_LEVEL} 사이여야 합니다.")
        
        return self._total_exp_cache.get(level, 0)
    
    def get_level_from_exp(self, total_exp: int) -> int:
        """
        총 경험치로부터 현재 레벨을 계산
        
        Args:
            total_exp: 총 누적 경험치
            
        Returns:
            int: 현재 레벨
        """
        if total_exp < 0:
            return 1
        
        # 이진 탐색으로 효율적으로 레벨 찾기
        left, right = 1, self.MAX_LEVEL
        current_level = 1
        
        while left <= right:
            mid = (left + right) // 2
            required_exp = self.total_exp_for_level(mid)
            
            if total_exp >= required_exp:
                current_level = mid
                left = mid + 1
            else:
                right = mid - 1
        
        return current_level
    
    def get_progress_to_next_level(self, total_exp: int) -> tuple:
        """
        다음 레벨까지의 진행률 정보
        
        Args:
            total_exp: 총 누적 경험치
            
        Returns:
            tuple: (현재 레벨, 현재 레벨 내 경험치, 다음 레벨까지 필요 경험치, 진행률%)
        """
        current_level = self.get_level_from_exp(total_exp)
        
        if current_level >= self.MAX_LEVEL:
            return current_level, 0, 0, 100.0
        
        current_level_total_exp = self.total_exp_for_level(current_level)
        next_level_total_exp = self.total_exp_for_level(current_level + 1)
        
        exp_in_current_level = total_exp - current_level_total_exp
        exp_needed_for_next = next_level_total_exp - current_level_total_exp
        exp_remaining = next_level_total_exp - total_exp
        
        progress_percent = (exp_in_current_level / exp_needed_for_next) * 100 if exp_needed_for_next > 0 else 100.0
        
        return current_level, exp_in_current_level, exp_remaining, progress_percent
    
    def add_experience(self, current_total_exp: int, gained_exp: int) -> dict:
        """
        경험치를 획득하고 레벨업 정보를 반환
        
        Args:
            current_total_exp: 현재 총 경험치
            gained_exp: 획득한 경험치
            
        Returns:
            dict: 레벨업 정보 및 변화량
        """
        old_level = self.get_level_from_exp(current_total_exp)
        new_total_exp = current_total_exp + gained_exp
        new_level = self.get_level_from_exp(new_total_exp)
        
        level_ups = new_level - old_level
        
        result = {
            "old_level": old_level,
            "new_level": new_level,
            "old_total_exp": current_total_exp,
            "new_total_exp": new_total_exp,
            "gained_exp": gained_exp,
            "level_ups": level_ups,
            "leveled_up": level_ups > 0
        }
        
        if level_ups > 0:
            result["stat_bonuses"] = self.calculate_level_up_bonuses(old_level, new_level)
        
        return result
    
    def calculate_level_up_bonuses(self, old_level: int, new_level: int) -> dict:
        """
        레벨업 시 스탯 보너스 계산
        
        Args:
            old_level: 이전 레벨
            new_level: 새 레벨
            
        Returns:
            dict: 스탯 증가량
        """
        level_diff = new_level - old_level
        
        # 기본 스탯 증가량 (레벨당)
        base_hp_per_level = 12
        base_mp_per_level = 6
        base_attack_per_level = 3
        base_defense_per_level = 2
        
        # 레벨 구간별 보너스 배율
        if new_level <= 25:
            multiplier = 1.0  # 초보자는 기본 증가량
        elif new_level <= 50:
            multiplier = 1.2  # 중급자는 20% 증가
        elif new_level <= 75:
            multiplier = 1.1  # 고급자는 10% 증가
        elif new_level <= 100:
            multiplier = 0.9  # 엔드게임은 90% (조금 감소)
        else:
            multiplier = 0.8  # 최고 레벨은 80% (더 완만)
        
        return {
            "hp": int(base_hp_per_level * level_diff * multiplier),
            "mp": int(base_mp_per_level * level_diff * multiplier),
            "attack": int(base_attack_per_level * level_diff * multiplier),
            "defense": int(base_defense_per_level * level_diff * multiplier)
        }
    
    def get_exp_progress_bar(self, total_exp: int, bar_length: int = 20) -> str:
        """
        경험치 진행률을 시각적 바로 표시
        
        Args:
            total_exp: 총 경험치
            bar_length: 바의 길이
            
        Returns:
            str: 진행률 바
        """
        current_level, exp_in_level, exp_remaining, progress = self.get_progress_to_next_level(total_exp)
        
        if current_level >= self.MAX_LEVEL:
            filled_bar = "■" * bar_length
            return f"[{filled_bar}] MAX"
        
        filled_length = int(bar_length * progress / 100)
        filled_bar = "■" * filled_length
        empty_bar = "□" * (bar_length - filled_length)
        
        return f"[{filled_bar}{empty_bar}] {progress:.1f}%"
    
    def get_level_info_display(self, total_exp: int) -> str:
        """
        레벨 정보를 보기 좋게 포맷팅
        
        Args:
            total_exp: 총 경험치
            
        Returns:
            str: 포맷된 레벨 정보
        """
        current_level, exp_in_level, exp_remaining, progress = self.get_progress_to_next_level(total_exp)
        
        if current_level >= self.MAX_LEVEL:
            return f"레벨 {current_level} (최대 레벨)"
        
        progress_bar = self.get_exp_progress_bar(total_exp)
        
        return (f"레벨 {current_level} {progress_bar}\n"
                f"다음 레벨까지: {exp_remaining:,} EXP")
    
    def get_recommended_exp_sources(self, current_level: int) -> list:
        """
        현재 레벨에 맞는 추천 경험치 소스
        
        Args:
            current_level: 현재 레벨
            
        Returns:
            list: 추천 활동 목록
        """
        if current_level <= 10:
            return [
                "🐭 들쥐정령 (18 EXP) - 한밭, 빛고을",
                "👻 떠돌이 혼 (15 EXP) - 한양, 아우내",
                "🎭 좀도깨비 (20 EXP) - 아우내, 한밭"
            ]
        elif current_level <= 25:
            return [
                "🦊 여우요괴 (35 EXP) - 소머리골, 한양",
                "🌊 물귀신 (30 EXP) - 제물포, 가마뫼",
                "🪶 까마귀요괴 (32 EXP) - 소머리골, 한양"
            ]
        elif current_level <= 50:
            return [
                "🌸 장화홍련 (45 EXP) - 한양, 빛고을",
                "🐸 무당개구리 (42 EXP) - 제물포, 가마뫼",
                "🏺 장승귀신 (50 EXP) - 아우내, 빛고을"
            ]
        else:
            return [
                "👹 어둑시니 (120 EXP) - 소머리골, 한밭",
                "🔥 불목도리 (140 EXP) - 가마뫼, 빛고을",
                "💀 묘혈수호령 (200 EXP) - 한양, 빛고을"
            ]


# 전역 경험치 시스템 인스턴스
exp_system = ExperienceSystem()


def get_exp_system():
    """경험치 시스템 인스턴스 반환"""
    return exp_system


# 편의 함수들
def calculate_level(total_exp: int) -> int:
    """총 경험치로 레벨 계산"""
    return exp_system.get_level_from_exp(total_exp)


def add_exp(current_total_exp: int, gained_exp: int) -> dict:
    """경험치 추가 및 레벨업 정보 반환"""
    return exp_system.add_experience(current_total_exp, gained_exp)


def get_level_display(total_exp: int) -> str:
    """레벨 정보 표시"""
    return exp_system.get_level_info_display(total_exp)


def get_recommended_activities(current_level: int) -> list:
    """현재 레벨에 맞는 추천 활동"""
    return exp_system.get_recommended_exp_sources(current_level) 