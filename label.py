from typing import Any
from ui_element import UIElement
from ui_manager_interface import UIManagerInterface

from pygame import font

class Label(UIElement):
    def __init__(self, ui_manager: UIManagerInterface, text: str="", x: int|str=0, y: int|str=0, width: int|str|None=None, height: int|str|None=None, anchor: str='top-left', visible: bool=True, parent: UIElement|None=None, theme_elements_name: list[str]|None=None, classes_names: list[str]|None=None) -> None:
        """
        A simple way to display text.
        """
        self._text = text
        self._font: font.Font|None = None
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('label')
        self._fit_text = self._text
        super().__init__(ui_manager, x, y, width, height, anchor, visible, parent, theme_elements_name, classes_names)

        self.can_have_focus = False
    
    def update_theme(self, theme_dict: dict[str, Any], erase: bool=False) -> None:
        super().update_theme(theme_dict, erase)
        self.update_font()

    def update_element(self) -> None:
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
        if not self._text:
            self._fit_text = ''
            return
        if self._relative_width:
            self._fit_text = self._text
        else:
            element_width = self._size[0]
            width = 0
            self._fit_text = ''
            for char in self._text:
                width = self._font.size(self._fit_text + char)[0]
                if width > element_width:
                    break
                self._fit_text += char
        if not self._relative_height:
            if self._font.size(self._fit_text)[1] + 2*self.border_width > self._size[1]:
                self._fit_text = ''

    def get_text_size(self) -> tuple[int, int]:
        if self._font is None:
            return (0, 0)
        return self._font.size(self._fit_text)

    def display_text(self) -> None:
        text_color = None
        if self.focus:
            text_color = self.get_theme_value('focused-text-color')
        if text_color is None and self.was_clicked:
            text_color = self.get_theme_value('clicked-text-color')
        if text_color is None and self.hovered:
            text_color = self.get_theme_value('hovered-text-color')
        if text_color is None:
            text_color = self.get_theme_value('text-color')
        text_size = self.get_text_size()
        start_x, start_y = 0, 0
        if self.get_theme_value('horizontal-center'):
            start_x = self._size[0] // 2 - text_size[0] // 2
        if self.get_theme_value('vertical-center'):
            start_y = self._size[1] // 2 - text_size[1] // 2
        self._ui_manager.get_window().blit(self._font
                    .render(self._fit_text,
                            self.get_theme_value('antialias'),
                            text_color),
                    (self._start_coords[0] + self.border_width + start_x,
                     self._start_coords[1] + self.border_width + start_y)
        )

    def get_content_size(self) -> tuple[int, int]:
        return self.get_text_size()

    def display(self) -> None:
        super().display()
        self.display_text()
    
    def set_text(self, text: str) -> None:
        self._text = text
        self.update_element()
        self._ui_manager.ask_refresh()
    
    def get_text(self) -> str:
        return self._text

    def update(self) -> None:
        if self.focus and self.get_theme_value('focused-text-color') is not None:
            self._ui_manager.ask_refresh(self)
        elif self.clicked and self.get_theme_value('clicked-text-color') is not None:
            self._ui_manager.ask_refresh(self)
        elif self.hovered and self.get_theme_value('hovered-text-color') is not None:
            self._ui_manager.ask_refresh(self)
        super().update()