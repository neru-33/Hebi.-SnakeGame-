from collections import deque
from game_logic.apple import Apple
from game_logic.snake import Snake


class GameState:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.snake = None
        self.apple = None
        self.score = 0
        self.game_over = False
        self.reset()

    def reset(self):
        # 화면 중앙에서 뱀 생성
        r, c = self.rows // 2, self.cols // 2
        start_body = deque([(r, c), (r, c - 1), (r, c - 2)])
        initial_direction = (0, 1)  # 오른쪽으로 시작

        self.snake = Snake(start_body, initial_direction)
        self.apple = Apple((0, 0))  # 임시 위치
        self.score = 0
        self.game_over = False
        self.apple.respawn(self.rows, self.cols, set(self.snake.body))

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
        if self.game_over:
            return

        # 1. 다음 상태 예측
        next_head_pos = self.snake.get_next_head_pos()
        grow = next_head_pos == self.apple.position

        # 2. 충돌 검사
        # 2-1. 벽 충돌
        if not (0 <= next_head_pos[0] < self.rows and 0 <= next_head_pos[1] < self.cols):
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
            self.apple.respawn(self.rows, self.cols, set(self.snake.body))

        # 승리 조건
        if len(self.snake.body) == self.rows * self.cols:
            self.game_over = True
            print("You Win!")

    def is_over(self) -> bool:
        return self.game_over

    def get_render_data(self) -> dict:
        return {
            "snake_body": list(self.snake.body),
            "apple_pos": self.apple.position,
            "score": self.score,
            "game_over": self.game_over,
        }
