import pygame
import sys
import time
import config
from game_logic.game_state import GameState
from rendering import (
    init_renderer,
    draw_frame,
    draw_overlay,
    draw_main_menu,
    draw_settings_screen,
    draw_pause_overlay,
)


def main():
    """
    메인 게임 함수. Pygame을 초기화하고 메인 게임 루프를 실행합니다.
    """
    pygame.init()

    # UI를 기준으로 초기 화면을 설정합니다. 게임 화면은 이보다 작을 수 있습니다.
    screen = pygame.display.set_mode((config.UI_SCREEN_WIDTH, config.UI_SCREEN_HEIGHT))
    pygame.display.set_caption("Hebi")
    clock = pygame.time.Clock()

    # --- 게임 상태 및 데이터 변수 ---
    game_state = None  # 실제 게임 로직과 데이터를 관리하는 객체
    game_surface = None  # 실제 게임이 그려질 별도의 Surface. UI와 분리됩니다.

    # --- 게임 상태(모드) 관리 ---
    # game_mode는 현재 게임이 어떤 상태인지를 나타냅니다 (예: 메인 메뉴, 게임 중).
    game_mode = "main_menu"
    # 설정 화면 등에서 이전 화면으로 돌아가기 위해 이전 상태를 저장합니다.
    previous_game_mode = None

    # 방향 키 입력을 실제 방향 벡터로 변환하기 위한 딕셔너리
    dir_map = {
        pygame.K_UP: (-1, 0),
        pygame.K_DOWN: (1, 0),
        pygame.K_LEFT: (0, -1),
        pygame.K_RIGHT: (0, 1),
    }

    # 고정된 시간 간격(Fixed Timestep)으로 게임 로직을 업데이트하기 위한 변수들
    last_time = time.perf_counter()
    accumulator = 0.0

    # --- UI 버튼 콜백(Callback) 함수들 ---
    # UI 버튼이 클릭되었을 때 실행될 함수들을 미리 정의합니다.
    # nonlocal 키워드를 사용하여 함수 외부의 변수(game_mode 등)를 수정합니다.
    def start_game():
        nonlocal game_mode
        game_mode = "gameplay"
        reset_game()

    def open_settings():
        nonlocal game_mode, previous_game_mode
        previous_game_mode = game_mode  # 현재 상태를 저장
        game_mode = "settings"

    def exit_game():
        nonlocal running
        running = False

    def back_to_main_menu():
        nonlocal game_mode
        game_mode = "main_menu"

    def resume_game():
        nonlocal game_mode
        game_mode = "gameplay"

    def back_from_settings():
        nonlocal game_mode, previous_game_mode
        # 설정 메뉴에 진입하기 전의 상태로 돌아갑니다.
        if previous_game_mode:
            game_mode = previous_game_mode
        else:
            game_mode = "main_menu"  # 비상시 메인 메뉴로 이동

    # --- 게임 초기화/재시작 함수 ---
    def reset_game():
        nonlocal game_state, game_surface, last_time, accumulator
        
        # config 파일에서 현재 UI에서 설정된 값들을 가져옵니다.
        game_config = config.get_current_config()
        
        # 현재 설정에 맞는 크기로 게임 화면용 Surface를 생성합니다.
        game_surface = pygame.Surface((game_config["SCREEN_WIDTH"], game_config["SCREEN_HEIGHT"]))
        
        # 설정 값을 전달하여 GameState 객체를 생성합니다.
        game_state = GameState(
            rows=game_config["GRID_ROWS"],
            cols=game_config["GRID_COLS"],
            max_apples=game_config["MAX_APPLES"],
        )
        # 렌더러를 초기화합니다.
        init_renderer(game_surface, game_config["GRID_COLS"], game_config["GRID_ROWS"])
        
        # 시간 변수들을 리셋하여 로직 업데이트가 처음부터 시작되도록 합니다.
        last_time = time.perf_counter()
        accumulator = 0.0

    # --- 메인 게임 루프 ---
    running = True
    while running:
        # --- 1. 이벤트 처리 ---
        # 매 프레임마다 발생하는 모든 이벤트를 가져옵니다 (키보드, 마우스 등).
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # ESC 키는 현재 게임 모드에 따라 다르게 동작합니다.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_mode == "gameplay":
                    game_mode = "paused"
                elif game_mode == "paused":
                    game_mode = "gameplay"
                elif game_mode == "settings":
                    back_from_settings()
                else: # main_menu
                    running = False

        # 매 프레임 시작 시 화면을 단색으로 채웁니다.
        screen.fill(config.BG_COLOR)

        # --- 2. 모드별 로직 및 렌더링 ---
        # 현재 game_mode에 따라 적절한 함수를 호출하여 화면을 그립니다.
        if game_mode == "main_menu":
            draw_main_menu(screen, start_game, open_settings, exit_game, events)

        elif game_mode == "settings":
            draw_settings_screen(screen, back_from_settings, events)

        elif game_mode == "gameplay" or game_mode == "paused":
            # 게임 플레이/일시정지 상태일 때의 로직
            if not game_state:
                reset_game()  # 첫 프레임일 경우 게임 초기화

            # 2-1. 게임 로직 업데이트 (일시정지 상태가 아닐 때만)
            if game_mode == "gameplay":
                # 사용자 입력 처리
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key in dir_map:
                        game_state.handle_input(dir_map[event.key])
                
                # 시간 기반 로직 업데이트 (고정된 시간 간격)
                game_config = config.get_current_config()
                tick_dt = 1.0 / (1000.0 / game_config["GAME_TICK_MS"])
                
                now = time.perf_counter()
                frame_time = now - last_time
                last_time = now
                accumulator += frame_time

                while accumulator >= tick_dt:
                    if not game_state.is_over() and not game_state.is_win():
                        game_state.update()
                    accumulator -= tick_dt

            # 2-2. 렌더링 (게임 플레이, 일시정지 모두)
            render_data = game_state.get_render_data()
            draw_frame(game_surface, render_data)

            # 게임 오버, 승리, 일시정지 등 추가적인 UI(오버레이)를 그립니다.
            if game_state.is_over():
                draw_overlay(game_surface, "game_over", game_state.score)
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        back_to_main_menu()
            elif game_state.is_win():
                draw_overlay(game_surface, "game_win", game_state.score)
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        back_to_main_menu()
            elif game_mode == "paused":
                draw_pause_overlay(game_surface, resume_game, open_settings, back_to_main_menu, events)
            
            # 최종적으로 게임 화면(game_surface)을 메인 화면(screen)의 중앙에 그립니다.
            pos_x = (screen.get_width() - game_surface.get_width()) // 2
            pos_y = (screen.get_height() - game_surface.get_height()) // 2
            screen.blit(game_surface, (pos_x, pos_y))

        # --- 3. 화면 업데이트 ---
        # 현재 프레임에 그려진 모든 것을 실제 화면에 표시합니다.
        pygame.display.flip()
        # FPS를 60으로 제한합니다.
        clock.tick(60)

    # 루프가 끝나면 Pygame을 종료합니다.
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
