import time
import random
import sys


def clear_screen():
    """화면을 지우는 함수"""
    print("\033[2J\033[H", end="")


def print_slowly(text, delay=0.03):
    """텍스트를 천천히 출력하는 함수"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def loading_bar(progress, total, bar_length=30):
    """진행률 바를 표시하는 함수"""
    filled_length = int(bar_length * progress // total)
    bar = "■" * filled_length + "□" * (bar_length - filled_length)
    percent = int(100 * progress / total)
    return f"[{bar}] {percent}%"


def game_startup_loading():
    """게임 시작 시 로딩 화면"""
    clear_screen()
    
    # 게임 타이틀
    print("\n" * 3)
    print("　" * 20 + "🌕 전란 그리고 요괴 🌕")
    print("　" * 15 + "조선시대 양란 직후의 혼란한 세상...")
    print("\n" * 2)
    
    loading_messages = [
        "📜 고서의 먼지를 털어내는 중...",
        "🏮 등불에 불을 밝히는 중...", 
        "⚔️ 무기를 준비하는 중...",
        "📿 부적을 그리는 중...",
        "🌸 벚꽃잎이 흩날리는 중...",
        "🏯 한양 성문을 여는 중...",
        "🎭 요괴들이 깨어나는 중...",
        "✨ 모험이 시작되는 중..."
    ]
    
    total_steps = len(loading_messages)
    
    for i, message in enumerate(loading_messages):
        print(f"　{message}")
        print(f"　{loading_bar(i + 1, total_steps)}")
        time.sleep(random.uniform(0.8, 1.5))
        
        if i < total_steps - 1:
            # 이전 두 줄 지우기
            print("\033[2A\033[K\033[K", end="")
    
    print("\n")
    print_slowly("　✨ 모든 준비가 완료되었습니다! ✨", 0.05)
    time.sleep(1)
    clear_screen()


def region_transition_loading(from_region, to_region):
    """지역 이동 시 로딩 화면"""
    clear_screen()
    
    print("\n" * 4)
    print("　" * 25 + "🚶‍♂️ 지역 이동 중 🚶‍♂️")
    print("　" * 20 + f"{from_region} → {to_region}")
    print("\n" * 2)
    
    # 지역별 특색 있는 로딩 메시지
    region_messages = {
        "한양": ["🏛️ 궁궐의 문이 열리는 중...", "👑 도성의 소음이 들려오는 중...", "🏮 상점가의 불빛이 보이는 중..."],
        "제물포": ["🌊 바닷바람이 불어오는 중...", "⛵ 배들이 항구에 도착하는 중...", "🐟 어부들의 노래가 들리는 중..."],
        "소머리골": ["🌲 깊은 산속으로 들어가는 중...", "👻 음산한 기운이 감도는 중...", "🦉 부엉이 울음소리가 들리는 중..."],
        "한밭": ["🌾 넓은 들판이 펼쳐지는 중...", "🦋 나비들이 날아다니는 중...", "⚡ 멀리서 번개가 치는 중..."],
        "빛고을": ["🌸 따뜻한 남쪽 바람이 부는 중...", "📚 학자들의 토론소리가 들리는 중...", "🌿 약초 향기가 풍기는 중..."],
        "가마뫼": ["🌋 화산의 열기가 느껴지는 중...", "♨️ 온천 김이 피어오르는 중...", "🔥 용암이 흐르는 소리가 들리는 중..."],
        "아우내": ["🛤️ 교차로에 도착하는 중...", "🏪 여관의 불빛이 보이는 중...", "🚶‍♀️ 여행자들과 마주치는 중..."],
        "탐라국": ["🏝️ 신비로운 섬이 보이는 중...", "🌺 이국적인 꽃향기가 나는 중...", "🦜 새로운 새 소리가 들리는 중..."]
    }
    
    # 목적지 지역의 메시지 선택
    messages = region_messages.get(to_region, ["🌟 새로운 장소로 향하는 중...", "👣 발걸음을 옮기는 중...", "🗺️ 길을 찾아가는 중..."])
    
    # 랜덤하게 메시지 선택
    selected_messages = random.sample(messages, min(3, len(messages)))
    
    for i, message in enumerate(selected_messages):
        print(f"　{message}")
        print(f"　{loading_bar(i + 1, len(selected_messages), 25)}")
        time.sleep(random.uniform(1.0, 1.8))
        
        if i < len(selected_messages) - 1:
            print("\033[2A\033[K\033[K", end="")
    
    print("\n")
    print_slowly(f"　🎯 {to_region}에 도착했습니다!", 0.05)
    time.sleep(1.2)
    clear_screen()


def battle_loading():
    """전투 시작 시 로딩 화면"""
    clear_screen()
    
    print("\n" * 4)
    print("　" * 25 + "⚔️ 전투 준비 중 ⚔️")
    print("\n" * 2)
    
    battle_messages = [
        "🗡️ 칼날을 벼리는 중...",
        "🛡️ 방어 자세를 취하는 중...",
        "✨ 기운을 모으는 중...",
        "👹 적이 나타나는 중..."
    ]
    
    for i, message in enumerate(battle_messages):
        print(f"　{message}")
        print(f"　{loading_bar(i + 1, len(battle_messages), 20)}")
        time.sleep(random.uniform(0.6, 1.0))
        
        if i < len(battle_messages) - 1:
            print("\033[2A\033[K\033[K", end="")
    
    print("\n")
    print_slowly("　💥 전투 시작! 💥", 0.05)
    time.sleep(0.8)
    clear_screen()


def save_loading():
    """저장 시 로딩 화면"""
    print("\n")
    print("　💾 게임을 저장하는 중...")
    
    save_steps = ["📝 데이터 정리 중...", "💾 파일 작성 중...", "✅ 저장 완료!"]
    
    for i, step in enumerate(save_steps):
        print(f"　{step}")
        print(f"　{loading_bar(i + 1, len(save_steps), 15)}")
        time.sleep(random.uniform(0.5, 1.0))
        
        if i < len(save_steps) - 1:
            print("\033[2A\033[K\033[K", end="")
    
    time.sleep(0.5)


def load_loading():
    """불러오기 시 로딩 화면"""
    print("\n")
    print("　📂 게임을 불러오는 중...")
    
    load_steps = ["🔍 파일 검색 중...", "📖 데이터 읽는 중...", "✨ 복원 완료!"]
    
    for i, step in enumerate(load_steps):
        print(f"　{step}")
        print(f"　{loading_bar(i + 1, len(load_steps), 15)}")
        time.sleep(random.uniform(0.5, 1.0))
        
        if i < len(load_steps) - 1:
            print("\033[2A\033[K\033[K", end="")
    
    time.sleep(0.5)


def random_travel_quote():
    """여행 중 표시할 랜덤 명언들"""
    quotes = [
        "천 리 길도 한 걸음부터 - 老子",
        "산 넘어 산이라 하되 그 산을 넘어가야지 - 속담",
        "가는 말이 고와야 오는 말이 곱다 - 속담", 
        "백문이 불여일견 - 漢書",
        "호랑이도 제 말 하면 온다 - 속담",
        "구슬이 서 말이라도 꿰어야 보배 - 속담",
        "천리길도 한걸음부터 시작된다 - 속담"
    ]
    
    return random.choice(quotes)


def enhanced_region_transition_loading(from_region, to_region):
    """향상된 지역 이동 로딩 화면 (명언 포함)"""
    region_transition_loading(from_region, to_region)
    
    # 이동 중 명언 표시
    print("\n" * 2)
    print("　" * 15 + "📜 여행자의 지혜 📜")
    print("　" * 10 + f'"{random_travel_quote()}"')
    print("\n")
    time.sleep(2)
    clear_screen() 