from collections import deque


class Snake:
    def __init__(self, start_body: deque, direction: tuple):
        self.body = start_body
        self.direction = direction
        self._next_direction = direction

    def head(self) -> tuple:
        return self.body[0]

    def set_direction(self, new_dir: tuple):
        # 현재 방향과 반대 방향이 아니면 다음 방향으로 예약
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self._next_direction = new_dir

    def get_next_head_pos(self) -> tuple:
        """
        다음 틱에서 머리가 위치할 좌표를 미리 계산합니다.
        """
        # 실제 이동 로직과 동일하게, 예약된 다음 방향을 기준으로 계산합니다.
        return (
            self.head()[0] + self._next_direction[0],
            self.head()[1] + self._next_direction[1],
        )

    def move(self, grow: bool):
        # 예약된 다음 방향을 현재 방향으로 업데이트
        self.direction = self._next_direction

        # get_next_head_pos와 중복 계산이지만, 로직 분리를 위해 유지
        new_head = (
            self.head()[0] + self.direction[0],
            self.head()[1] + self.direction[1],
        )
        self.body.appendleft(new_head)
        if not grow:
            self.body.pop()

    def is_self_collision(self, next_head_pos: tuple, is_growing: bool) -> bool:
        """
        다음 머리 위치가 자기 몸과 충돌하는지 확인합니다.
        """
        if is_growing:
            # 성장할 때는 꼬리가 그대로 있으므로 몸 전체와 비교
            return next_head_pos in self.body
        else:
            # 성장하지 않을 때는 꼬리가 한 칸 움직이므로, 꼬리를 제외하고 비교
            body_without_tail = list(self.body)[:-1]
            return next_head_pos in body_without_tail
