from ui_manager_interface import UIManagerInterface
from ui_element import UIElement
from label import Label

from typing import Callable

class Button(Label):
    def __init__(self, ui_manager: UIManagerInterface, text: str="", on_click_function: Callable[["Button"], None]|None=None, x: int|str=0, y: int|str=0, width: int|str|None=None, height: int|str|None=None, anchor: str='top-left', visible: bool=True, parent: UIElement|None=None, theme_elements_name: list[str]|None=None, classes_names: list[str]|None=None) -> None:
        """
        A button who display a text and who can be clicked.
        If 'on_click_function' is given, the function will be called on click.
        """
        self._on_click_function = on_click_function
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('button')
        super().__init__(ui_manager, text, x, y, width, height, anchor, visible, parent, theme_elements_name, classes_names)
    

    def update(self) -> None:
        if self.unclicked and self._on_click_function is not None:
            self._on_click_function(self)
        super().update()
