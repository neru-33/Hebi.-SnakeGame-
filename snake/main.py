from __future__ import annotations
import argparse
import random
import time
import pygame as pg

import config
from game_logic import GameState  ##인터페이스 클래스
from rendering import Renderer  ##인터페이스 클래스


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Snake Game(pygame)")
    p.add_argument("--rows", type=int, default=config.ROWS)
    p.add_argument("--cols", type=int, default=config.COLS)
    p.add_argument("--cell-size", type=int, default=config.CELL_SIZE)
    p.add_argument("--fps", type=int, default=config.FPS)
    p.add_argument("--tick", type=float, default=config.TICK)
    p.add_argument("--seed", type=int, default=config.SEED)
    p.add_argument("--no-sound", action="store_true", default=config.NO_SOUND)
    p.add_argument("--windowed", action="store_true", default=config.WINDOWED)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    pg.init()
    if not args.no_sound:
        try:
            pg.mixer.init()
        except Exception:
            pass

    width = args.cols * args.cell_size
    height = args.rows * args.cell_size

    flags = pg.SCALED | pg.RESIZABLE
    screen = pg.display.set_mode((width, height), flags)
    pg.display.set_caption("Snake (Pygame)")

    clock = pg.time.Clock()

    state = GameState(rows=args.rows, cols=args.cols)
    renderer = Renderer(
        screen=screen, cell_size=args.cell_size, rows=args.rows, cols=args.cols
    )

    dir_map = {
        # (행,열) 순서. 행은 아래로 증가
        pg.K_UP: (-1, 0),
        pg.K_DOWN: (1, 0),
        pg.K_LEFT: (0, -1),
        pg.K_RIGHT: (0, 1),
        # wasd 키 입력 추가할 경우 이곳에 추가
        # pg.K_w:(-1, 0), ...
    }

    paused = False
    show_overlay = True
    running = True

    tick_rate = max(1e-3, float(args.tick))
    tick_dt = 1.0 / tick_rate
    acc = 0.0
    last_time = time.perf_counter()

    try:
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key in dir_map and not paused:
                        state.handle_input(dir_map[event.key])
                    elif event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_SPACE:
                        paused = not paused
                    elif event.key == pg.K_TAB:
                        show_overlay = not show_overlay
                    elif event.key == pg.K_r and state.is_game_over:
                        state = GameState(rows=args.rows, cols=args.cols)

        now = time.perf_counter()
        frame_dt = now - last_time
        last_time = now
        acc += frame_dt

        if not paused and not state.is_game_over:
            while acc >= tick_dt:
                state.update()
                acc -= tick_dt

        screen.fill((18, 18, 18))
        renderer.draw(state)
        if show_overlay:
            renderer.draw_overlay(fps=clock.get_fps(), paused=paused)

        pg.display.flip()
        clock.tick(args.fps)

    finally:
        pg.quit()


if __name__ == "__main__":
    main()
