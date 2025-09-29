import pygame
from typing import Dict, Tuple, List, Literal, Callable
import config
from ui import Button
import os

# --- 모듈 수준 변수 ---
# 렌더링에 필요한 폰트, 오프셋, UI 요소들을 전역적으로 관리합니다.
_font = None
_title_font = None
_offset_x = 0
_offset_y = 0

# --- 이미지 텍스처 로드 ---
_textures = {}

def _load_textures():
    """
    게임에 사용될 이미지 텍스처들을 로드하고 크기를 조절합니다.
    """
    global _textures
    if _textures:
        return
    
    # 이미지 파일 경로를 생성합니다.
    # os.path.join을 사용하여 OS에 맞는 경로 구분자를 사용합니다.
    # '..'을 사용하여 'snake' 디렉토리에서 상위 디렉토리로 이동 후 'res'로 들어갑니다.
    base_path = os.path.join(os.path.dirname(__file__), '..', 'res')
    
    try:
        # 텍스처들을 딕셔너리에 로드합니다.
        _textures = {
            'tile': pygame.image.load(os.path.join(base_path, 'tile.png')).convert(),
            'apple': pygame.image.load(os.path.join(base_path, 'apple.png')).convert_alpha(),
            'body': pygame.image.load(os.path.join(base_path, 'body.png')).convert_alpha(),
            # 방향 벡터: (row, col)
            (0, 1): pygame.image.load(os.path.join(base_path, 'head_right.png')).convert_alpha(),      # 오른쪽
            (0, -1): pygame.image.load(os.path.join(base_path, 'head_left.png')).convert_alpha(), # 왼쪽
            (-1, 0): pygame.image.load(os.path.join(base_path, 'head_up.png')).convert_alpha(), # 위
            (1, 0): pygame.image.load(os.path.join(base_path, 'head_down.png')).convert_alpha(),  # 아래
        }

        # 로드된 모든 이미지의 크기를 TILE_SIZE에 맞게 조절합니다.
        tile_dim = (config.TILE_SIZE, config.TILE_SIZE)
        for key, img in _textures.items():
            _textures[key] = pygame.transform.scale(img, tile_dim)

    except pygame.error as e:
        print(f"텍스처 파일 로딩 중 오류 발생: {e}")
        # 오류 발생 시 _textures를 비워 텍스처 렌더링을 시도하지 않도록 합니다.
        _textures = {}


# UI 요소들은 한 번만 생성하고 재사용하여 성능을 최적화합니다.
_main_menu_buttons = []
_settings_elements = []
_pause_menu_buttons = []


def _initialize_fonts():
    """
    게임에 필요한 폰트들을 초기화합니다. (최초 한 번만 실행)
    """
    global _font, _title_font
    if _font and _title_font:
        return
    try:
        _font = pygame.font.SysFont("malgungothic", config.FONT_SIZE)
        _title_font = pygame.font.SysFont("malgungothic", config.TITLE_FONT_SIZE)
    except pygame.error:
        print("'맑은 고딕' 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")
        _font = pygame.font.Font(None, config.FONT_SIZE)
        _title_font = pygame.font.Font(None, config.TITLE_FONT_SIZE)


def init_renderer(screen: pygame.Surface, grid_cols: int, grid_rows: int) -> None:
    """
    게임 플레이 화면 렌더링을 초기화합니다.
    게임 그리드를 화면 중앙에 맞추기 위한 오프셋을 계산합니다.
    """
    global _offset_x, _offset_y
    _initialize_fonts()
    _load_textures() # 텍스처 로딩 함수 호출

    grid_width = grid_cols * config.TILE_SIZE
    grid_height = grid_rows * config.TILE_SIZE
    _offset_x = (screen.get_width() - grid_width) // 2
    _offset_y = (screen.get_height() - grid_height) // 2


def _init_ui_elements(
    start_game_cb: Callable, open_settings_cb: Callable, exit_game_cb: Callable,
    back_from_settings_cb: Callable, resume_game_cb: Callable, go_to_main_menu_cb: Callable,
):
    """
    메인 메뉴, 설정, 일시정지 메뉴의 모든 UI 요소(버튼)들을 초기화합니다.
    최초 호출 시 버튼 객체들을 생성하고, 이후에는 콜백 함수만 최신으로 업데이트합니다.
    """
    global _main_menu_buttons, _settings_elements, _pause_menu_buttons
    _initialize_fonts()

    if _main_menu_buttons: # 이미 생성된 경우 콜백만 업데이트
        _main_menu_buttons[0].callback = start_game_cb
        _main_menu_buttons[1].callback = open_settings_cb
        _main_menu_buttons[2].callback = exit_game_cb
        _settings_elements[-1]["button"].callback = back_from_settings_cb
        _pause_menu_buttons[0].callback = resume_game_cb
        _pause_menu_buttons[1].callback = open_settings_cb
        _pause_menu_buttons[2].callback = go_to_main_menu_cb
        return

    # --- UI 요소 생성 (최초 한 번만 실행) ---
    center_x = config.UI_SCREEN_WIDTH // 2
    btn_w, btn_h = 200, 50
    
    # 1. 메인 메뉴 버튼
    start_y = config.UI_SCREEN_HEIGHT // 2 - 50
    _main_menu_buttons = [
        Button(pygame.Rect(center_x - btn_w // 2, start_y, btn_w, btn_h), "게임 시작", _font, start_game_cb),
        Button(pygame.Rect(center_x - btn_w // 2, start_y + 60, btn_w, btn_h), "설정", _font, open_settings_cb),
        Button(pygame.Rect(center_x - btn_w // 2, start_y + 120, btn_w, btn_h), "게임 종료", _font, exit_game_cb),
    ]

    # 2. 설정 화면 UI 요소
    _settings_elements = []
    setting_y = 150
    setting_items = {"speed": ("속도", config.SPEED_OPTIONS), "map_size": ("맵 크기", config.MAP_SIZE_OPTIONS), "apple_count": ("사과 개수", config.APPLE_COUNT_OPTIONS)}
    for key, (label, options) in setting_items.items():
        def create_callback(setting_key, option_list):
            def on_click():
                # 현재 설정 값과 다른 값으로 변경될 때만 플래그를 설정합니다.
                current_value = config.current_settings[setting_key]
                current_idx = option_list.index(current_value)
                next_idx = (current_idx + 1) % len(option_list)
                new_value = option_list[next_idx]
                
                if current_value != new_value:
                    config.current_settings[setting_key] = new_value
                    config.settings_have_changed = True
            return on_click
        option_keys = list(options.keys())
        btn = Button(pygame.Rect(center_x - 125, setting_y, 250, 40), f"{label}: {config.current_settings[key]}", _font, create_callback(key, option_keys))
        _settings_elements.append({"label": label, "key": key, "button": btn})
        setting_y += 60
    back_btn = Button(pygame.Rect(center_x - 100, setting_y + 20, 200, 50), "뒤로가기", _font, back_from_settings_cb)
    _settings_elements.append({"button": back_btn})

    # 3. 일시정지 메뉴 버튼
    _pause_menu_buttons = [
        Button(pygame.Rect(0, 0, 180, 40), "게임 재개", _font, resume_game_cb),
        Button(pygame.Rect(0, 0, 180, 40), "설정", _font, open_settings_cb),
        Button(pygame.Rect(0, 0, 180, 40), "메인 메뉴로", _font, go_to_main_menu_cb),
    ]


def draw_main_menu(screen: pygame.Surface, start_game_cb: Callable, open_settings_cb: Callable, exit_game_cb: Callable, events: List[pygame.event.Event]) -> None:
    """메인 메뉴 화면을 그립니다."""
    _init_ui_elements(start_game_cb, open_settings_cb, exit_game_cb, lambda: None, lambda: None, lambda: None)
    title_surf = _title_font.render("Hebi", True, config.UI_TITLE_COLOR)
    title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
    screen.blit(title_surf, title_rect)
    for button in _main_menu_buttons:
        for event in events:
            button.handle_event(event)
        button.draw(screen)


def draw_settings_screen(screen: pygame.Surface, back_from_settings_cb: Callable, events: List[pygame.event.Event]) -> None:
    """설정 화면을 그립니다."""
    _init_ui_elements(lambda: None, lambda: None, lambda: None, back_from_settings_cb, lambda: None, lambda: None)
    title_surf = _title_font.render("설정", True, config.UI_TITLE_COLOR)
    title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 80))
    screen.blit(title_surf, title_rect)
    for element in _settings_elements:
        button = element["button"]
        if "key" in element: # 설정 값 변경 시 버튼 텍스트 업데이트
            button.text = f"{element['label']}: {config.current_settings[element['key']]}"
        for event in events:
            button.handle_event(event)
        button.draw(screen)


def draw_frame(screen: pygame.Surface, render_data: Dict) -> None:
    """한 프레임의 게임 화면(뱀, 사과, 점수)을 그립니다."""
    screen.fill(config.BG_COLOR)
    if not _font: return

    game_config = config.get_current_config()

    # --- 타일 배경 그리기 ---
    if _textures.get('tile'):
        for r in range(game_config["GRID_ROWS"]):
            for c in range(game_config["GRID_COLS"]):
                _draw_tile(screen, (r, c), _textures['tile'])

    # --- 맵 경계선 그리기 ---
    border_rect = pygame.Rect(
        _offset_x, 
        _offset_y, 
        game_config["GRID_COLS"] * config.TILE_SIZE, 
        game_config["GRID_ROWS"] * config.TILE_SIZE
    )
    pygame.draw.rect(screen, config.GRID_COLOR, border_rect, 1)

    # --- 게임 요소 그리기 ---
    # 텍스처가 성공적으로 로드되었는지 확인합니다.
    if not _textures:
        # 텍스처 로딩 실패 시 기존의 사각형 방식으로 그립니다 (Fallback)
        for apple_pos in render_data.get("apples", []):
            _draw_tile_fallback(screen, apple_pos, config.APPLE_COLOR)
        snake_parts = render_data.get("snake_body", [])
        if snake_parts:
            _draw_tile_fallback(screen, snake_parts[0], config.SNAKE_HEAD_COLOR)
            for part in snake_parts[1:]:
                _draw_tile_fallback(screen, part, config.SNAKE_BODY_COLOR)
    else:
        # 텍스처를 사용하여 그립니다.
        for apple_pos in render_data.get("apples", []):
            _draw_tile(screen, apple_pos, _textures['apple'])
        
        snake_parts = render_data.get("snake_body", [])
        snake_direction = render_data.get("snake_direction")

        if snake_parts:
            # 머리 그리기: 방향에 맞는 텍스처를 선택합니다.
            head_texture = _textures.get(snake_direction, _textures.get((0, 1))) # 방향 키가 없으면 오른쪽(기본)
            if head_texture:
                _draw_tile(screen, snake_parts[0], head_texture)
            
            # 몸통 그리기
            if _textures.get('body'):
                for part in snake_parts[1:]:
                    _draw_tile(screen, part, _textures['body'])
    
    score_surf = _font.render(f"점수: {render_data.get('score', 0)}", True, (255, 255, 255))
    screen.blit(score_surf, (10, 10))

def _draw_tile(screen: pygame.Surface, pos: Tuple[int, int], texture: pygame.Surface) -> None:
    """그리드 좌표에 맞는 위치에 텍스처를 그리는 헬퍼 함수입니다."""
    r, c = pos
    rect = pygame.Rect(
        _offset_x + c * config.TILE_SIZE, 
        _offset_y + r * config.TILE_SIZE, 
        config.TILE_SIZE, 
        config.TILE_SIZE
    )
    screen.blit(texture, rect)

def _draw_tile_fallback(screen: pygame.Surface, pos: Tuple[int, int], color: Tuple[int, int, int]) -> None:
    """[Fallback] 그리드 좌표에 맞는 사각형 타일 하나를 그리는 헬퍼 함수입니다."""
    r, c = pos
    rect = pygame.Rect(
        _offset_x + c * config.TILE_SIZE, 
        _offset_y + r * config.TILE_SIZE, 
        config.TILE_SIZE, 
        config.TILE_SIZE
    )
    pygame.draw.rect(screen, color, rect)



def draw_overlay(screen: pygame.Surface, state: Literal["game_over", "game_win"], score: int) -> None:
    """게임 오버 또는 승리 시 나타나는 반투명 오버레이를 그립니다."""
    overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay_surface.fill((0, 0, 0, 128))
    if not _font: return
    if state == "game_over":
        title_text = "게임 오버"
        prompt_text = "재시작: Enter / 메뉴로: ESC"
    else: # game_win
        title_text = "게임 승리"
        prompt_text = "메인 메뉴로 돌아가려면 Enter를 누르세요"

    subtitle_text = f"최종 점수: {score}"
    texts = [
        (_title_font.render(title_text, True, (255, 255, 255)), -50),
        (_font.render(subtitle_text, True, (255, 255, 255)), 10),
        (_font.render(prompt_text, True, (200, 200, 200)), 60),
    ]
    center_x, center_y = screen.get_width() / 2, screen.get_height() / 2
    for surf, offset_y in texts:
        rect = surf.get_rect(center=(center_x, center_y + offset_y))
        overlay_surface.blit(surf, rect)
    screen.blit(overlay_surface, (0, 0))


def draw_pause_overlay(screen: pygame.Surface, resume_game_cb: Callable, open_settings_cb: Callable, go_to_main_menu_cb: Callable, events: List[pygame.event.Event]) -> None:
    """일시정지 메뉴 오버레이를 그립니다."""
    overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay_surface.fill((0, 0, 0, 128))
    if not _font: return

    _init_ui_elements(lambda:None, open_settings_cb, lambda:None, lambda:None, resume_game_cb, go_to_main_menu_cb)

    title_surf = _title_font.render("일시정지", True, (255, 255, 255))
    center_x, center_y = screen.get_width() / 2, screen.get_height() / 2
    title_rect = title_surf.get_rect(center=(center_x, center_y - 100))
    overlay_surface.blit(title_surf, title_rect)

    # 버튼들의 위치를 중앙에 맞추고 그립니다.
    for i, button in enumerate(_pause_menu_buttons):
        button.rect.center = (center_x, center_y + (i * 60) - 20)
        for event in events:
            button.handle_event(event)
        button.draw(overlay_surface)

    screen.blit(overlay_surface, (0, 0))


def draw_restart_prompt_overlay(screen: pygame.Surface) -> None:
    """설정 변경 후 재시작이 필요하다는 안내 오버레이를 그립니다.""" 
    overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay_surface.fill((0, 0, 0, 170)) # 좀 더 진한 배경
    if not _font: return

    prompt_text = "설정이 변경되었습니다. Enter를 눌러 재시작하세요."
    
    prompt_surf = _font.render(prompt_text, True, (255, 255, 255))
    prompt_rect = prompt_surf.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    overlay_surface.blit(prompt_surf, prompt_rect)

    screen.blit(overlay_surface, (0, 0))



