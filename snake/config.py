"""
게임의 주요 설정을 담는 파일입니다.
색상, 크기, 속도 등 상수를 정의합니다.
"""

# --- SEED 값 (None일 경우 System Time 사용) ---
SEED = 10
# SEED = None

# --- 화면 및 그리드 설정 ---
GRID_COLS = 30  # 그리드 너비 (타일 개수)
GRID_ROWS = 20  # 그리드 높이 (타일 개수)
TILE_SIZE = 20  # 각 타일의 크기 (픽셀)

SCREEN_WIDTH = GRID_COLS * TILE_SIZE
SCREEN_HEIGHT = GRID_ROWS * TILE_SIZE

# --- 색상 정의 (RGB) ---
BG_COLOR = (20, 20, 20)  # 배경색
APPLE_COLOR = (255, 50, 50)  # 사과색
SNAKE_HEAD_COLOR = (0, 200, 0)  # 뱀 머리색
SNAKE_BODY_COLOR = (0, 150, 0)  # 뱀 몸통색
GRID_COLOR = (40, 40, 40)  # 그리드 선 색상 (선택 사항)

# --- 폰트 설정 ---
FONT_PATH = None  # None으로 설정 시 Pygame 기본 폰트 사용
FONT_SIZE = 24

# --- 게임 플레이 설정 ---
GAME_TICK_MS = 150  # 게임 틱 간격 (밀리초). 작을수록 빨라짐
MAX_APPLES = 5  # 화면에 나타날 최대 사과 개수
