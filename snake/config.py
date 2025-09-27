"""
게임의 주요 설정을 담는 파일입니다.
색상, 크기, 속도 등 상수를 정의합니다.
"""

# --- SEED 값 (None일 경우 System Time 사용) ---
# 테스트 시 동일한 사과 위치를 보장하기 위해 고정된 SEED 값을 사용합니다.
SEED = 10
# SEED = None

# --- 화면 기본 설정 ---
# 이 값들은 UI 화면의 최대 크기를 결정하며, 게임 화면은 이보다 작거나 같을 수 있습니다.
MAX_GRID_COLS = 40
MAX_GRID_ROWS = 30
TILE_SIZE = 20

# UI 화면 크기는 최대 그리드 크기를 기준으로 고정됩니다.
UI_SCREEN_WIDTH = MAX_GRID_COLS * TILE_SIZE
UI_SCREEN_HEIGHT = MAX_GRID_ROWS * TILE_SIZE


# --- 색상 정의 (RGB) ---
BG_COLOR = (20, 20, 20)
APPLE_COLOR = (255, 50, 50)
SNAKE_HEAD_COLOR = (0, 200, 0)
SNAKE_BODY_COLOR = (0, 150, 0)
GRID_COLOR = (40, 40, 40)
# UI 관련 색상 추가
UI_TEXT_COLOR = (220, 220, 220)
UI_BUTTON_COLOR = (80, 80, 80)
UI_BUTTON_HOVER_COLOR = (110, 110, 110)
UI_TITLE_COLOR = (100, 220, 100)


# --- 폰트 설정 ---
FONT_PATH = None  # None으로 설정 시 Pygame 기본 폰트 사용
FONT_SIZE = 24
TITLE_FONT_SIZE = 48

# --- 게임 플레이 설정 옵션 ---
# 사용자가 UI에서 선택할 수 있는 옵션들을 미리 정의합니다.
# 각 옵션은 UI에 표시될 이름(key)과 실제 게임 로직에 사용될 값(value)으로 구성됩니다.
SPEED_OPTIONS = {
    "느림": 200,  # 게임 틱 간격 (ms)
    "보통": 150,
    "빠름": 100,
}

MAP_SIZE_OPTIONS = {
    "작게": (20, 15),  # (가로 타일 수, 세로 타일 수)
    "보통": (30, 20),
    "크게": (40, 30),
}

APPLE_COUNT_OPTIONS = {
    "적게": 3,  # 화면에 나타날 최대 사과 개수
    "보통": 5,
    "많게": 10,
}

# --- 현재 게임 설정 (딕셔너리) ---
# 프로그램 실행 중에 UI를 통해 이 딕셔너리의 값이 변경됩니다.
# 기본값으로 '보통' 난이도를 설정합니다.
current_settings = {
    "speed": "보통",
    "map_size": "보통",
    "apple_count": "보통",
}


def get_current_config() -> dict:
    """
    UI에서 선택된 현재 설정(예: "보통")을 기반으로,
    게임 로직에 필요한 실제 값(예: 150)들을 계산하여 딕셔너리 형태로 반환합니다.
    이 함수를 통해 게임 시작 및 재시작 시 동적으로 변경된 설정을 적용할 수 있습니다.
    """
    map_cols, map_rows = MAP_SIZE_OPTIONS[current_settings["map_size"]]

    return {
        "GAME_TICK_MS": SPEED_OPTIONS[current_settings["speed"]],
        "MAX_APPLES": APPLE_COUNT_OPTIONS[current_settings["apple_count"]],
        "GRID_COLS": map_cols,
        "GRID_ROWS": map_rows,
        "SCREEN_WIDTH": map_cols * TILE_SIZE,
        "SCREEN_HEIGHT": map_rows * TILE_SIZE,
    }
