from collections import deque
from game_logic.snake import Snake
import config
import random


class GameState:
    """
    게임의 모든 상태와 핵심 로직을 관리하는 클래스입니다.
    뱀, 사과, 점수, 게임 오버 여부 등 게임의 모든 데이터를 포함하며,
    게임의 규칙에 따라 이 데이터들을 업데이트하는 역할을 합니다.
    """
    def __init__(self, rows: int, cols: int, max_apples: int):
        """
        GameState 객체를 초기화합니다.
        :param rows: 게임 그리드의 세로 크기
        :param cols: 게임 그리드의 가로 크기
        :param max_apples: 화면에 동시에 존재할 수 있는 최대 사과 개수
        """
        self.rows = rows
        self.cols = cols
        self.max_apples = max_apples
        self.snake = None
        self.apples = []
        self.score = 0
        self.game_over = False
        self.game_win = False
        self.reset()

    def reset(self):
        """
        게임 상태를 초기 상태로 리셋합니다.
        게임 시작 또는 재시작 시 호출됩니다.
        """
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

        # 설정된 개수만큼 사과를 생성합니다.
        for _ in range(self.max_apples):
            self._spawn_apple()

    def _spawn_apple(self):
        """
        맵의 빈 공간(뱀이나 다른 사과가 없는 위치)에 새로운 사과를 하나 생성합니다.
        만약 빈 공간이 없다면 아무것도 하지 않습니다.
        """
        total_cells = self.rows * self.cols
        occupied_cells = len(self.snake.body) + len(self.apples)
        if occupied_cells >= total_cells:
            return  # 빈 공간이 없으면 함수 종료

        # 뱀의 몸통과 현재 사과들의 위치를 제외한 곳에 새 사과를 생성합니다.
        occupied_positions = set(self.snake.body) | set(self.apples)
        while True:
            new_pos = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            if new_pos not in occupied_positions:
                self.apples.append(new_pos)
                break

    def handle_input(self, next_dir: tuple):
        """
        사용자 입력을 받아 뱀의 다음 방향을 설정합니다.
        """
        if next_dir:
            self.snake.set_direction(next_dir)

    def update(self):
        """
        게임 상태를 한 틱(tick) 업데이트합니다. 이 함수는 고정된 시간 간격으로 호출됩니다.
        로직: [예측] -> [충돌 검사] -> [실행]
        """
        if self.game_over or self.game_win:
            return

        # 1. [예측] 뱀이 다음 틱에 어디로 갈지 예측합니다.
        next_head_pos = self.snake.get_next_head_pos()
        grow = next_head_pos in self.apples  # 사과를 먹는지 여부

        # 2. [충돌 검사] 예측된 위치가 유효한지 검사합니다.
        # 2-1. 벽 충돌 검사
        if not (0 <= next_head_pos[0] < self.rows and 0 <= next_head_pos[1] < self.cols):
            self.game_over = True
            return
        # 2-2. 자기 몸 충돌 검사
        if self.snake.is_self_collision(next_head_pos, grow):
            self.game_over = True
            return

        # 3. [실행] 충돌이 없다면, 예측된 상태를 실제 게임 상태에 반영합니다.
        self.snake.move(grow)

        if grow:
            self.score += 1
            self.apples.remove(next_head_pos)  # 먹은 사과 제거
            self._spawn_apple()  # 새 사과 추가

        # 승리 조건: 뱀의 몸통이 전체 그리드를 가득 채웠을 때
        if len(self.snake.body) == self.rows * self.cols:
            self.game_win = True
            return

    def is_win(self) -> bool:
        return self.game_win

    def is_over(self) -> bool:
        return self.game_over

    def get_render_data(self) -> dict:
        """
        현재 게임 상태 데이터를 렌더링 모듈에 전달하기 위한 딕셔너리를 반환합니다.
        이를 통해 게임 로직과 렌더링 로직을 분리할 수 있습니다.
        """
        return {
            "snake_body": list(self.snake.body),
            "snake_direction": self.snake.direction,
            "apples": self.apples,
            "score": self.score,
            "game_over": self.game_over,
            "game_win": self.game_win,
        }
