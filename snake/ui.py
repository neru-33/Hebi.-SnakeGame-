import pygame
from typing import Tuple, Callable
import config


class Button:
    """
    UI에서 사용될 클릭 가능한 버튼을 나타내는 클래스입니다.
    버튼의 위치, 크기, 텍스트, 색상 및 클릭 시 실행될 동작(콜백 함수)을 관리합니다.
    """

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        callback: Callable = None,
        bg_color: Tuple[int, int, int] = config.UI_BUTTON_COLOR,
        hover_color: Tuple[int, int, int] = config.UI_BUTTON_HOVER_COLOR,
        text_color: Tuple[int, int, int] = config.UI_TEXT_COLOR,
    ):
        """
        버튼 객체를 초기화합니다.
        :param rect: 버튼의 위치와 크기를 담은 pygame.Rect 객체
        :param text: 버튼에 표시될 텍스트
        :param font: 텍스트 렌더링에 사용될 pygame.font.Font 객체
        :param callback: 버튼 클릭 시 호출될 함수 (콜백)
        """
        self.rect = rect
        self.text = text
        self.font = font
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False  # 마우스가 버튼 위에 있는지 여부

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        주어진 pygame 이벤트를 처리합니다.
        마우스 움직임에 따라 호버 상태를 업데이트하고, 마우스 클릭 시 콜백 함수를 실행합니다.
        """
        if event.type == pygame.MOUSEMOTION:
            # 마우스 커서가 버튼 영역 안에 있는지 확인
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 버튼이 호버된 상태에서 마우스 좌클릭이 발생했는지 확인
            if self.is_hovered and event.button == 1:
                if self.callback:
                    # 등록된 콜백 함수가 있다면 실행
                    self.callback()

    def draw(self, screen: pygame.Surface) -> None:
        """
        버튼을 화면에 그립니다.
        마우스 호버 상태에 따라 다른 배경색을 사용합니다.
        """
        # 1. 버튼 배경 그리기
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        # 2. 버튼 텍스트 그리기 (중앙 정렬)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
