from collections import deque

class snake:
    def __init__(self, start_pos: tuple, direction: tuple):
        self.body = deque([start_pos])
        self.direction = direction

    def head(self) -> tuple:
        return self.body[0]

    def set_direction(self, new_dir: tuple):
        # 역방향으로의 즉각적인 전환을 방지
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def move(self, grow: bool):
        new_head = (self.head()[0] + self.direction[0], self.head()[1] + self.direction[1])
        self.body.appendleft(new_head)
        if not grow:
            self.body.pop()

    def collides(self, pos: tuple) -> bool:
        # 꼬리가 이번 턴에 빠질 예정이고 그 칸으로 들어가는 경우는 예외 (허용)
        # 뱀의 몸통이 2개 이상일 때만 자기 몸 충돌 체크
        if len(self.body) > 1:
            # 새로운 머리 좌표가 꼬리를 제외한 나머지 몸통에 있는지 확인
            return self.head() in list(self.body)[1:]
        return False