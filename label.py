from ui_element import UIElement
from ui_manager import UIManager

from pygame import font

class Label(UIElement):
    def __init__(self, ui_manager: UIManager, text: str="", start_x: int|None=None, start_y: int|None=None, width: int|None=None, height: int|None=None, horizontal_center: bool=False, vertical_center: bool=False, visible: bool=True, parent: UIElement|None=None, theme_elements_name: list[str]|None=None) -> None:
        """
        A simple way to display text.
        """
        self._text = text
        self._font: font.SysFont|None = None
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('label')
        self._fit_text = self._text
        super().__init__(ui_manager, start_x, start_y, width, height, horizontal_center, vertical_center, visible, parent, theme_elements_name)

        self.can_have_focus = False
    
    def update_element(self) -> None:
        self.update_font()
        self.update_fit_text()
        super().update_element()

    def update_font(self) -> None:
        self._font = font.SysFont(
            self.get_theme_value('font-name'),
            self.get_theme_value('font-size')
        )

    def update_fit_text(self) -> None:
        """
        Set in 'self._fit_text' the text who can be entirely displayed with the actual size
        """
        if self._relative_width:
            self._fit_text = self._text
        else:
            element_width = self._size[0] - self.get_theme_value('edges-width') * 2
            width = 0
            for i, char in enumerate(self._text, 1):
                width += self._font.size(char)[0]
                if width > element_width:
                    i -= 1
                    break
            self._fit_text = self._text[:i]
        if not self._relative_height:
            if self._font.size(self._fit_text)[1] > self._size[1]:
                self._fit_text = ''

    def get_text_size(self) -> tuple[int, int]:
        if self._font is None:
            return (0, 0)
        return self._font.size(self._fit_text)

    def display_text(self) -> None:
        self._ui_manager.window.blit(self._font
            .render(self._fit_text, True, "#ffffff"), (self._start_coords[0] + self.get_theme_value('edges-width'), self._start_coords[1] + self.get_theme_value('edges-width')))

    def get_content_size(self) -> tuple[int, int]:
        return self.get_text_size()

    def display(self) -> None:
        self.display_text()
        self.display_edge()
    
