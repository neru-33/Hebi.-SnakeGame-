import pygame
import sys
import time
import config
from game_logic.game_state import GameState
from rendering import init_renderer, draw_frame, draw_overlay


def main():
    """
    메인 게임 함수. 게임 루프를 초기화하고 실행합니다.
    """
    pygame.init()

    # 화면 설정
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Hebi - Snake Game")
    clock = pygame.time.Clock()

    # 게임 상태 및 렌더러 초기화
    game_state = GameState(config.GRID_ROWS, config.GRID_COLS)
    init_renderer(screen, config.GRID_COLS, config.GRID_ROWS)

    # 방향 키 매핑
    dir_map = {
        pygame.K_UP: (-1, 0),
        pygame.K_DOWN: (1, 0),
        pygame.K_LEFT: (0, -1),
        pygame.K_RIGHT: (0, 1),
    }

    # 시간 기반 게임 루프 설정
    tick_rate = 1.0 / (config.GAME_TICK_MS / 1000.0)
    tick_dt = 1.0 / tick_rate
    last_time = time.perf_counter()
    accumulator = 0.0

    running = True
    while running:
        # --- 입력 처리 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game_state.is_over():
                    if event.key == pygame.K_RETURN:
                        game_state.reset()
                elif event.key in dir_map:
                    game_state.handle_input(dir_map[event.key])

        # --- 로직 업데이트 (시간 기반) ---
        now = time.perf_counter()
        frame_time = now - last_time
        last_time = now
        accumulator += frame_time

        while accumulator >= tick_dt:
            if not game_state.is_over():
                game_state.update()
            accumulator -= tick_dt

        # --- 렌더링 ---
        render_data = game_state.get_render_data()
        draw_frame(
            screen,
            {
                "snake": render_data["snake_body"],
                "apple": render_data["apple_pos"],
                "score": render_data["score"],
            },
        )

        if game_state.is_over():
            draw_overlay(screen, "game_over", game_state.score)

        pygame.display.flip()

        # FPS 제한
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
