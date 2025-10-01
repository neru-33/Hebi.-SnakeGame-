from collections import deque


class Snake:
    """
    뱀의 데이터와 동작을 관리하는 클래스입니다.
    뱀의 몸통 위치, 현재 이동 방향, 다음 이동 방향 등을 관리합니다.
    """
    def __init__(self, start_body: deque, direction: tuple):
        """
        Snake 객체를 초기화합니다.
        :param start_body: 뱀의 초기 몸통 위치를 담은 deque
        :param direction: 뱀의 초기 이동 방향 (예: (0, 1)은 오른쪽)
        """
        self.body = start_body  # 뱀의 몸통. deque의 왼쪽 끝(index 0)이 머리입니다.
        self.direction = direction  # 현재 뱀이 움직이는 방향
        self._next_direction = direction  # 다음 틱에 적용될 방향 (입력 버퍼 역할)

    def head(self) -> tuple:
        """뱀의 머리 좌표를 반환합니다."""
        return self.body[0]

    def set_direction(self, new_dir: tuple):
        """
        사용자 입력을 받아 뱀의 다음 방향을 예약합니다.
        뱀이 현재 이동 방향의 정반대로 즉시 움직이는 것을 방지합니다.
        """
        # 현재 방향과 반대 방향이 아니면 다음 방향으로 예약
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self._next_direction = new_dir

    def set_direction_if_collision(self):
        """
        충돌 시 머리 방향을 렌더링 하기 위해 현재 방향을 업데이트 합니다.
        """
        self.direction = self._next_direction

    def get_next_head_pos(self) -> tuple:
        """
        다음 틱에서 머리가 위치할 좌표를 미리 계산하여 반환합니다.
        GameState에서 충돌 검사를 위해 사용됩니다.
        """
        # 실제 이동 로직과 동일하게, 예약된 다음 방향(_next_direction)을 기준으로 계산합니다.
        return (
            self.head()[0] + self._next_direction[0],
            self.head()[1] + self._next_direction[1],
        )

    def move(self, grow: bool):
        """
        뱀을 한 칸 이동시킵니다.
        :param grow: True이면 꼬리를 제거하지 않아 몸이 길어집니다.
        """
        # 1. 예약된 다음 방향을 현재 방향으로 업데이트합니다.
        #    이를 통해 사용자가 한 틱에 여러 번 키를 눌러도 마지막 유효한 입력만 반영됩니다.
        self.direction = self._next_direction

        # 2. 새로운 머리 위치를 계산합니다.
        new_head = (
            self.head()[0] + self.direction[0],
            self.head()[1] + self.direction[1],
        )
        # 3. 새로운 머리를 몸통의 맨 앞에 추가합니다.
        self.body.appendleft(new_head)

        # 4. 성장(grow)하지 않는 경우, 꼬리를 한 칸 제거합니다.
        if not grow:
            self.body.pop()

    def is_self_collision(self, next_head_pos: tuple, is_growing: bool) -> bool:
        """
        다음 머리 위치가 자기 몸과 충돌하는지 확인합니다.
        :param next_head_pos: 검사할 다음 머리의 위치
        :param is_growing: 뱀이 다음 틱에 성장하는지 여부
        """
        if is_growing:
            # 성장할 때는 꼬리가 그대로 남아있으므로, 몸 전체와 충돌하는지 확인합니다.
            return next_head_pos in self.body
        else:
            # 성장하지 않을 때는 꼬리가 한 칸 앞으로 움직일 예정이므로,
            # 현재의 꼬리 위치는 다음 틱에 비어있게 됩니다. 따라서 꼬리를 제외하고 충돌을 검사합니다.
            body_without_tail = list(self.body)[:-1]
            return next_head_pos in body_without_tail
