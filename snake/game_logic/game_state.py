from collections import deque
from game_logic.snake import Snake
import config
import random


class GameState:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.snake = None
        self.apples = []
        self.score = 0
        self.game_over = False
        self.game_win = False
        self.reset()

    def reset(self):
        if config.SEED is not None:
            random.seed(config.SEED)

        # 화면 중앙에서 뱀 생성
        r, c = self.rows // 2, self.cols // 2
        start_body = deque([(r, c), (r, c - 1), (r, c - 2)])
        initial_direction = (0, 1)  # 오른쪽으로 시작

        self.snake = Snake(start_body, initial_direction)
        self.apples = []
        self.score = 0
        self.game_over = False
        self.game_win = False

        # 설정된 개수만큼 사과 생성
        for _ in range(config.MAX_APPLES):
            self._spawn_apple()

    def _spawn_apple(self):
        """
        맵의 빈 공간에 새로운 사과를 하나 생성합니다.
        만약 빈 공간이 없다면 아무것도 하지 않습니다.
        """
        # 1. 안전 장치: 빈 공간이 있는지 확인
        total_cells = self.rows * self.cols
        occupied_cells = len(self.snake.body) + len(self.apples)

        if occupied_cells >= total_cells:
            return  # 빈 공간이 없으므로 함수 종료

        # 2. 사과 생성
        occupied_positions = set(self.snake.body) | set(self.apples)
        while True:
            new_pos = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            if new_pos not in occupied_positions:
                self.apples.append(new_pos)
                break

    def handle_input(self, next_dir: tuple):
        """
        입력을 받아 뱀의 다음 방향을 설정합니다.
        """
        if next_dir:
            self.snake.set_direction(next_dir)

    def update(self):
        """
        게임 상태를 한 틱 업데이트합니다. (예측 -> 충돌 검사 -> 실행)
        """
        if self.game_over or self.game_win:
            return

        # 1. 다음 상태 예측
        next_head_pos = self.snake.get_next_head_pos()
        grow = next_head_pos in self.apples

        # 2. 충돌 검사
        # 2-1. 벽 충돌
        if not (
            0 <= next_head_pos[0] < self.rows and 0 <= next_head_pos[1] < self.cols
        ):
            self.game_over = True
            return
        # 2-2. 자기 몸 충돌
        if self.snake.is_self_collision(next_head_pos, grow):
            self.game_over = True
            return

        # 3. 상태 실행 (충돌이 없을 경우)
        self.snake.move(grow)

        if grow:
            self.score += 1
            self.apples.remove(next_head_pos)  # 먹은 사과 제거
            self._spawn_apple()  # 새 사과 추가

        # 승리 조건
        if len(self.snake.body) == self.rows * self.cols:
            self.game_win = True
            return

    def is_win(self) -> bool:
        return self.game_win

    def is_over(self) -> bool:
        return self.game_over

    def get_render_data(self) -> dict:
        return {
            "snake_body": list(self.snake.body),
            "apples": self.apples,
            "score": self.score,
            "game_over": self.game_over,
            "game_win": self.game_win,
        }
