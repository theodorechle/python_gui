from ui_manager import UIManager
from ui_element import UIElement
import pygame

class Slider(UIElement):
    DEFAULT_STEP_SIZE: int = 5 # in pixels
    DEFAULT_HEIGHT: int = 10
    def __init__(self, ui_manager: UIManager, min_value: int, max_value: int, step: int|float|None=None, round_precision: int|None=None, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None, anchor: str = 'top-left', visible: bool = True, parent: UIElement | None = None, theme_elements_name: list[str] | None = None) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value:int|float = self.min_value
        self.round_precision = round_precision
        self.cursor_radius = self.DEFAULT_HEIGHT
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('slider')
        super().__init__(ui_manager, x, y, width, height, anchor, visible, parent, theme_elements_name)
        self.can_have_focus = True
        self.value_x = 0

    def get_content_size(self) -> tuple[int, int]:
        nb_values = self.max_value - self.min_value
        if self._relative_width:
            length = self.DEFAULT_STEP_SIZE*nb_values + self.cursor_radius + self.border_width*2
        else:
            length = self._size[0]
        if self._relative_height:
            height = self.DEFAULT_HEIGHT + self.cursor_radius + self.border_width*2
        else:
            height = self._size[1]
            self.cursor_radius = height//2 - self.border_width
        return (length, height)
    
    def update(self) -> None:
        super().update()
        if self.was_clicked:
            self.set_value()

    def set_value(self) -> None:
        x = pygame.mouse.get_pos()[0]
        x -= self._start_coords[0]
        x -= self.cursor_radius
        x = min(self._size[0] - self.cursor_radius * 2, max(0, x))
        self.value_x = x
        if self.step:
            size_step = (self._size[0] - self.cursor_radius * 2) / ((self.max_value - self.min_value) / self.step)
            x /= size_step
            x *= self.step
            x += self.min_value
        else:
            x = 100 * x / self._size[0]
        if self.round_precision is not None:
            x = round(x, self.round_precision)
        self.value = x
        self._ui_manager.ask_refresh(self)

    def display(self) -> None:
        super().display()
        self.display_bar()
        self.display_cursor()
    
    def display_bar(self) -> None:
        pygame.draw.rect(
            self._ui_manager.get_window(),
            self.get_theme_value('bar-color'),
            pygame.Rect(
                self._start_coords[0] + self.cursor_radius // 2,
                self._start_coords[1] + self.cursor_radius // 2,
                self._size[0] - self.cursor_radius,
                self._size[1] - self.cursor_radius
            ),
            self.get_theme_value('border-radius'),
            self.get_theme_value('border-top-left-radius'),
            self.get_theme_value('border-top-right-radius'),
            self.get_theme_value('border-bottom-left-radius'),
            self.get_theme_value('border-bottom-right-radius')
        )
    
    def display_cursor(self) -> None:
        pygame.draw.circle(
            self._ui_manager.get_window(),
            self.get_theme_value('cursor-color'),
            (self.value_x + self._start_coords[0] + self.cursor_radius, self._start_coords[1] + self.cursor_radius + self.border_width),
            self.cursor_radius
        )