# 📄game_logic
📌 개요

`game_logic.py`는 스네이크 게임의 **핵심 로직**을 담당하는 모듈이다.

- **UI/렌더링**, **입력 처리**와는 독립적이어야 한다.
- 이 모듈은 뱀(`Snake`), 보드(`Board`), 사과(`Apple`)의 상태와 동작을 정의하며,
    
    `GameState` 클래스에서 이를 조율한다.
    
- 외부(main loop, rendering)는 **GameState**만 사용하면 된다.

---

## 📂 클래스 구조

### 1. `Snake`

- **역할**: 뱀의 몸통 좌표와 이동 로직 관리
- **필드**
    - `body: deque[(int, int)]` → 머리부터 꼬리까지 좌표
    - `direction: (int, int)` → 현재 이동 방향 (dr, dc)
- **메서드**
    - `head() -> (int, int)` : 머리 좌표 반환
    - `set_direction(new_dir: (int, int))` : 새로운 방향 설정 (역방향 입력 무시 가능)
    - `move(grow: bool)` : 머리를 한 칸 이동, grow=True이면 꼬리 유지(길이+1)
    - `collides(pos: (int, int)) -> bool` : 주어진 좌표가 몸통과 겹치는지 확인

---

### 2. `Board`

- **역할**: 격자 공간의 크기와 충돌/스폰 관리
- **필드**
    - `rows: int`, `cols: int`
- **메서드**
    - `in_bounds(pos: (int, int)) -> bool` : 주어진 좌표가 보드 안인지 확인
    - `random_empty_cell(occupied: set[(int,int)]) -> (int, int)` : 비어있는 셀 중 무작위 반환

---

### 3. `Apple`

- **역할**: 사과 아이템의 위치 관리
- **필드**
    - `position: (int, int)`
- **메서드**
    - `respawn(board: Board, occupied: set[(int,int)])` : 비어있는 칸에 사과 재배치

---

### 4. `GameState`

- **역할**: Snake, Board, Apple을 묶어 한 판의 진행 상태를 관리
- **필드**
    - `snake: Snake`
    - `board: Board`
    - `apple: Apple`
    - `score: int`
    - `game_over: bool`
- **메서드**
    - `__init__(rows: int, cols: int)` : 보드 크기 지정 후 초기화
    - `reset()` : 새 게임으로 초기화
    - `tick(next_dir: Optional[(int, int)])`
        - 입력 방향을 반영하여 한 턴 진행
        - 충돌 판정, 사과 처리, 점수 업데이트
    - `is_over() -> bool` : 게임오버 여부 확인
    - `get_render_data() -> dict` : 렌더링 모듈에 전달할 데이터 패키징
        - 예시:
            
            ```python
            {
              "snake": [(r,c), ...],
              "apple": (r,c),
              "score": int,
              "game_over": bool
            }
            
            ```
            

---

## 📌 게임 진행 규칙 (내부 로직)

1. **이동**
    - Snake가 현재 방향으로 머리를 1칸 이동한다.
    - `grow=True` (사과 먹음) → 꼬리를 유지
    - `grow=False` → 꼬리 한 칸 제거
2. **충돌 판정**
    - 벽 충돌: 머리가 보드 밖이면 게임오버
    - 자기몸 충돌:
        - 새 머리가 몸통에 포함되면 게임오버
        - 단, 꼬리가 이번 턴에 빠질 예정이고 그 칸으로 들어가는 경우는 예외 (허용)
3. **사과**
    - 새 머리 == 사과 위치 → 점수 +1, grow=True, Apple 재배치
    - Snake 길이가 보드 전체와 같아지면 **승리** 처리 (game_over=True)

---

## 📌 외부에서 사용하는 API

- `state = GameState(rows, cols)`
- `state.tick(next_dir)`
- `state.get_render_data()` → 렌더링에서 사용
- `state.is_over()` → 게임오버 확인
- `state.reset()` → 새 게임 시작

---

## ✅ 테스트 체크리스트

- [ ]  Snake가 빈칸 이동 시 정상적으로 꼬리 제거
- [ ]  사과를 먹으면 길이 증가 + 점수 증가
- [ ]  벽 충돌 시 game_over=True
- [ ]  자기 몸 충돌 시 game_over=True
- [ ]  사과를 먹지 않은 턴에 꼬리 칸으로 이동하는 경우 합법 처리
- [ ]  보드 전체 채우면 game_over=True (승리)