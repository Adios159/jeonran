#!/usr/bin/env python3
"""
전란 그리고 요괴 - 성능 벤치마크 도구
최적화 전후 성능 비교 측정
"""

import time
import tracemalloc
import sys
import json
from typing import Dict, List, Callable


class PerformanceBenchmark:
    """성능 벤치마크 클래스"""
    
    def __init__(self):
        self.results: Dict[str, Dict] = {}
        self.current_test = None
    
    def run_test(self, test_name: str, test_function: Callable, iterations: int = 1000):
        """성능 테스트 실행"""
        print(f"🔍 테스트 실행 중: {test_name}")
        
        # 메모리 추적 시작
        tracemalloc.start()
        
        # 시간 측정
        start_time = time.perf_counter()
        
        for _ in range(iterations):
            test_function()
        
        end_time = time.perf_counter()
        
        # 메모리 사용량 측정
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # 결과 저장
        execution_time = (end_time - start_time) / iterations * 1000  # ms
        
        self.results[test_name] = {
            'execution_time_ms': round(execution_time, 3),
            'memory_current_mb': round(current / 1024 / 1024, 2),
            'memory_peak_mb': round(peak / 1024 / 1024, 2),
            'iterations': iterations
        }
        
        print(f"✅ 완료: {execution_time:.3f}ms (평균)")
    
    def compare_tests(self, baseline: str, optimized: str):
        """두 테스트 결과 비교"""
        if baseline not in self.results or optimized not in self.results:
            print("❌ 비교할 테스트 결과가 없습니다.")
            return
        
        baseline_result = self.results[baseline]
        optimized_result = self.results[optimized]
        
        time_improvement = (
            (baseline_result['execution_time_ms'] - optimized_result['execution_time_ms']) /
            baseline_result['execution_time_ms'] * 100
        )
        
        memory_improvement = (
            (baseline_result['memory_peak_mb'] - optimized_result['memory_peak_mb']) /
            baseline_result['memory_peak_mb'] * 100
        )
        
        print(f"\n📊 **성능 비교: {baseline} vs {optimized}**")
        print("=" * 50)
        print(f"실행 시간 개선: {time_improvement:+.1f}%")
        print(f"메모리 사용량 개선: {memory_improvement:+.1f}%")
        print(f"절대 시간 단축: {baseline_result['execution_time_ms'] - optimized_result['execution_time_ms']:.3f}ms")
    
    def generate_report(self):
        """성능 리포트 생성"""
        print(f"\n📋 **성능 벤치마크 리포트**")
        print("=" * 60)
        
        for test_name, result in self.results.items():
            print(f"\n🔹 {test_name}")
            print(f"   실행 시간: {result['execution_time_ms']:.3f}ms")
            print(f"   메모리 사용량: {result['memory_current_mb']:.2f}MB")
            print(f"   최대 메모리: {result['memory_peak_mb']:.2f}MB")
            print(f"   반복 횟수: {result['iterations']}")
    
    def save_results(self, filename: str = "benchmark_results.json"):
        """결과를 파일로 저장"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"💾 결과 저장: {filename}")


def benchmark_data_loading():
    """데이터 로딩 성능 테스트"""
    benchmark = PerformanceBenchmark()
    
    # 기존 방식 (개별 JSON 로딩)
    def old_loading():
        import json
        import os
        
        data = {}
        for filename in ['data/items.json', 'data/weapons.json', 'data/shops.json']:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data[filename] = json.load(f)
    
    # 최적화된 방식 (중앙화된 로딩)
    def new_loading():
        try:
            from systems.data_manager import get_data
            get_data('items')
            get_data('weapons')
            get_data('shops')
        except ImportError:
            pass  # 시스템이 없는 경우 스킵
    
    benchmark.run_test("기존_데이터_로딩", old_loading, 100)
    benchmark.run_test("최적화_데이터_로딩", new_loading, 100)
    benchmark.compare_tests("기존_데이터_로딩", "최적화_데이터_로딩")
    
    return benchmark


def benchmark_inventory_operations():
    """인벤토리 연산 성능 테스트"""
    benchmark = PerformanceBenchmark()
    
    # 기존 인벤토리
    def old_inventory_test():
        try:
            from systems.inventory import Inventory
            inv = Inventory()
            for i in range(10):
                inv.add_item(f"아이템_{i}", 1)
                inv.get_used_capacity()  # 매번 계산
        except ImportError:
            pass
    
    # 최적화된 인벤토리
    def new_inventory_test():
        try:
            from systems.inventory_optimized import OptimizedInventory
            inv = OptimizedInventory()
            for i in range(10):
                inv.add_item(f"아이템_{i}", 1)
                inv.get_used_capacity()  # 캐시된 계산
        except ImportError:
            pass
    
    benchmark.run_test("기존_인벤토리", old_inventory_test, 1000)
    benchmark.run_test("최적화_인벤토리", new_inventory_test, 1000)
    benchmark.compare_tests("기존_인벤토리", "최적화_인벤토리")
    
    return benchmark


def main():
    """메인 벤치마크 실행"""
    print("🚀 전란 그리고 요괴 - 성능 벤치마크")
    print("=" * 50)
    
    try:
        # 데이터 로딩 벤치마크
        print("\n1️⃣ 데이터 로딩 성능 테스트")
        data_benchmark = benchmark_data_loading()
        
        # 인벤토리 벤치마크
        print("\n2️⃣ 인벤토리 연산 성능 테스트")
        inventory_benchmark = benchmark_inventory_operations()
        
        # 통합 리포트
        print("\n📊 **통합 성능 리포트**")
        data_benchmark.generate_report()
        inventory_benchmark.generate_report()
        
        # 결과 저장
        all_results = {**data_benchmark.results, **inventory_benchmark.results}
        with open("performance_results.json", 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        print("\n✅ 벤치마크 완료!")
        print("📁 결과 파일: performance_results.json")
        
    except Exception as e:
        print(f"❌ 벤치마크 오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 