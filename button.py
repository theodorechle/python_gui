from ui_manager import UIManager
from ui_element import UIElement
from label import Label

from typing import Callable

class Button(Label):
    def __init__(self, ui_manager: UIManager, text: str="", on_click_function: Callable[["Button"], None]|None=None, start_x: int|None=None, start_y: int|None=None, width: int|None=None, height: int|None=None, horizontal_center: bool=False, vertical_center: bool=False, visible: bool=True, parent: UIElement|None=None, theme_elements_name: list[str]|None=None) -> None:
        """
        A button who display a text and who can be clicked.
        If 'on_click_function' is given, the function will be called on click.
        """
        self._on_click_function = on_click_function
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('button')
        super().__init__(ui_manager, text, start_x, start_y, width, height, horizontal_center, vertical_center, visible, parent, theme_elements_name)
    

    def update(self) -> None:
        if self.unclicked and self._on_click_function is not None:
            self._on_click_function(self)
        super().update()
