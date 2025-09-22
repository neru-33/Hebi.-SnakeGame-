import pygame
from typing import Dict, Tuple, List, Literal

from config import (
    BG_COLOR,
    APPLE_COLOR,
    SNAKE_HEAD_COLOR,
    SNAKE_BODY_COLOR,
    TILE_SIZE,
    FONT_PATH,
    FONT_SIZE,
)

# --- 렌더링 리소스를 위한 모듈 수준 변수 ---
_font = None
_offset_x = 0
_offset_y = 0


def init_renderer(screen: pygame.Surface, grid_cols: int, grid_rows: int) -> None:
    """
    폰트와 같은 렌더링 리소스를 초기화하고 레이아웃 오프셋을 계산합니다.
    """
    global _font, _offset_x, _offset_y
    try:
        # 시스템 폰트(맑은 고딕)를 우선적으로 시도하고, 실패 시 기본 폰트를 사용합니다.
        _font = pygame.font.SysFont("malgungothic", FONT_SIZE)
    except pygame.error:
        print(
            f"'맑은 고딕' 폰트를 찾을 수 없어 기본 폰트를 사용합니다. (한글이 깨질 수 있습니다)"
        )
        _font = pygame.font.Font(None, FONT_SIZE)

    # 그리드를 화면 중앙에 맞추기 위한 오프셋 계산
    grid_width = grid_cols * TILE_SIZE
    grid_height = grid_rows * TILE_SIZE
    _offset_x = (screen.get_width() - grid_width) // 2
    _offset_y = (screen.get_height() - grid_height) // 2


def draw_frame(screen: pygame.Surface, render_data: Dict) -> None:
    """
    제공된 render_data를 기반으로 단일 게임 프레임을 그립니다.
    """
    screen.fill(BG_COLOR)

    if not render_data:
        # render_data가 없는 경우 처리
        if _font:
            text_surf = _font.render("게임 데이터 없음", True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=screen.get_rect().center)
            screen.blit(text_surf, text_rect)
        return

    # 사과 그리기
    apple_pos = render_data.get("apple")
    if apple_pos:
        _draw_tile(screen, apple_pos, APPLE_COLOR)

    # 뱀 그리기
    snake_parts = render_data.get("snake", [])
    if snake_parts:
        # 머리
        _draw_tile(screen, snake_parts[0], SNAKE_HEAD_COLOR)
        # 몸통
        for part in snake_parts[1:]:
            _draw_tile(screen, part, SNAKE_BODY_COLOR)

    # HUD (점수) 그리기
    score = render_data.get("score", 0)
    if _font:
        score_surf = _font.render(f"점수: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))


def draw_overlay(
    screen: pygame.Surface,
    state: Literal["pause", "game_over", "ready", "game_win"],
    score: int,
) -> None:
    """
    메시지와 함께 반투명 오버레이를 그립니다.
    """
    overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay_surface.fill((0, 0, 0, 128))  # 반투명 검정

    if not _font:
        return  # 폰트 없이는 텍스트를 그릴 수 없음

    if state == "game_over":
        title_text = "게임 오버"
        subtitle_text = f"최종 점수: {score}"
        prompt_text = "다시 시작하려면 Enter를 누르세요"
    if state == "game_win":
        title_text = "1121212"
        subtitle_text = f"111 점수: {score}"
        prompt_text = "다시 시작하려면 Enter를 누르세요"
    elif state == "pause":
        title_text = "일시정지"
        prompt_text = "계속하려면 P를 누르세요"
        subtitle_text = ""
    else:  # ready
        title_text = "Hebi"
        subtitle_text = "화살표 키로 이동"
        prompt_text = "시작하려면 Enter를 누르세요"

    # 제목
    title_surf = _font.render(title_text, True, (255, 255, 255))
    title_rect = title_surf.get_rect(
        center=(screen.get_width() / 2, screen.get_height() / 2 - 50)
    )
    overlay_surface.blit(title_surf, title_rect)

    # 부제
    if subtitle_text:
        subtitle_surf = _font.render(subtitle_text, True, (255, 255, 255))
        subtitle_rect = subtitle_surf.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        overlay_surface.blit(subtitle_surf, subtitle_rect)

    # 프롬프트
    prompt_surf = _font.render(prompt_text, True, (200, 200, 200))
    prompt_rect = prompt_surf.get_rect(
        center=(screen.get_width() / 2, screen.get_height() / 2 + 50)
    )
    overlay_surface.blit(prompt_surf, prompt_rect)

    screen.blit(overlay_surface, (0, 0))


def teardown_renderer() -> None:
    """
    렌더링 리소스를 정리합니다.
    """
    global _font
    _font = None


def _draw_tile(
    screen: pygame.Surface, pos: Tuple[int, int], color: Tuple[int, int, int]
) -> None:
    """
    단일 그리드 타일을 그리는 헬퍼 함수입니다.
    """
    r, c = pos
    rect = pygame.Rect(
        _offset_x + c * TILE_SIZE, _offset_y + r * TILE_SIZE, TILE_SIZE, TILE_SIZE
    )
    pygame.draw.rect(screen, color, rect)
