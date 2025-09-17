# 📄 Rendering

## 📌 개요

`rendering.py`는 **화면 그리기 전담** 모듈이다. 게임 상태(`GameState`)를 **읽기만** 하며, 게임 로직을 변경하지 않는다. 모든 Pygame `Surface` 조작과 폰트/스프라이트 로딩, 레이아웃 계산을 담당한다.

---

## 📦 외부 의존성

- `pygame` (display, surface, font)
- 프로젝트 내부: `config.py` (색상, 타일 크기, 폰트 경로/크기 등)

---

## 🧩 공개 API

### `init_renderer(screen: pygame.Surface, grid_cols: int, grid_rows: int) -> None`

- **역할:** 폰트/이미지 등 렌더 자원 초기화. 화면 해상도에 따른 그리드 스케일 계산.
- **사이드 이펙트:** 내부 모듈 전역(또는 렌더러 객체)의 폰트/레이아웃 캐시 준비.

### `draw_frame(screen: pygame.Surface, render_data: dict) -> None`

- **입력 규약:** `GameState.get_render_data()` 반환값을 그대로 받음.
    - `render_data["snake"]`: `[(r, c), ...]` (머리→꼬리)
    - `render_data["apple"]`: `(r, c)`
    - `render_data["score"]`: `int`
    - `render_data["game_over"]`: `bool`
- **역할:** 배경 → 그리드(선택) → 사과 → 뱀(머리/몸/꼬리) → HUD 순서로 그리기.
- **주의:** 상태를 변경하지 말 것. 예외 발생 시 표시용 fallback UI 유지.

### `draw_overlay(screen: pygame.Surface, state: Literal["pause","game_over","ready"], score: int) -> None`

- **역할:** 반투명 오버레이와 메시지(“Paused”, “Game Over”, “Press Enter to restart” 등) 표시.
- **입력:** 오버레이 종류, 점수.

### `teardown_renderer() -> None`

- **역할:** 폰트/이미지 등 캐시 정리(필요 시). 일반적으로 Pygame 종료는 `main`이 수행.

---

## 🎨 표현 규칙

- **그리드→픽셀 변환:**
    
    `rect = (offset_x + c * TILE, offset_y + r * TILE, TILE, TILE)`
    
- **색상(예시):**
    - 배경: `BG_COLOR`
    - 그리드선(옵션): `GRID_COLOR` (얇게)
    - 사과: `APPLE_COLOR`
    - 뱀 머리: `SNAKE_HEAD_COLOR`
    - 뱀 몸: `SNAKE_BODY_COLOR`
- **HUD:** 좌상단에 점수, 우상단에 속도/틱(선택). 폰트는 `config.FONT_PATH`, `config.FONT_SIZE`.
- **애니메이션(선택):** 머리 깜빡임, 먹을 때 잠깐 팝 효과 등은 **순수 렌더링에서만** 처리(상태 미변경).

---

## ⚠️ 에러/엣지 처리

- `render_data` 누락 시: 안전한 기본값으로 그리기(빈 화면 + “No Data” 텍스트).
- 해상도 변경(리사이즈) 옵션 지원 시 `init_renderer` 재호출로 스케일 재계산.

---

## ✅ 테스트 체크리스트

- [ ]  빈 상태에서도 예외 없이 프레임 렌더
- [ ]  긴 뱀(수십 타일)에서도 60fps 근처
- [ ]  오버레이 on/off 시 Z-order 정상
- [ ]  다른 해상도에서도 타일 경계 정렬(블러 없음)