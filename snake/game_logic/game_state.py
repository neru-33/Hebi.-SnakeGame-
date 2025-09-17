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
        start_pos = (self.rows // 2, self.cols // 2)
        initial_direction = (0, 1)  # 오른쪽으로 시작
        self.snake = Snake(start_pos, initial_direction)
        self.apple = Apple((0, 0))  # 임시 위치
        self.score = 0
        self.game_over = False
        self.apple.respawn(self.rows, self.cols, set(self.snake.body))

    def tick(self, next_dir: tuple):
        if self.game_over:
            return

        # 입력 방향 반영
        self.snake.set_direction(next_dir)

        # 뱀 이동
        grow = False
        # 사과 위치와 뱀의 다음 머리 위치가 같으면
        new_head = (
            self.snake.head()[0] + self.snake.direction[0],
            self.snake.head()[1] + self.snake.direction[1],
        )
        if new_head == self.apple.position:
            self.score += 1
            grow = True

        self.snake.move(grow)

        # 충돌 판정 (벽)
        if not (
            0 <= self.snake.head()[0] < self.rows
            and 0 <= self.snake.head()[1] < self.cols
        ):
            self.game_over = True
            return

        # 충돌 판정 (자기 몸)
        if self.snake.collides(self.snake.head()):
            self.game_over = True
            return

        # 사과 처리
        if grow:
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
