from ui_manager_interface import UIManagerInterface
from ui_element import UIElement
from container import Container
from pygame import Surface
from typing import Callable
from copy import copy

class Button(Container):
    def __init__(
            self,
            ui_manager: UIManagerInterface,
            on_click_function: Callable[["Button"], None]|None=None,
            x: int|str=0,
            y: int|str=0,
            width: int|str|None=None,
            height: int|str|None=None,
            anchor: str='top-left',
            visible: bool=True,
            parent: UIElement|None=None,
            theme_elements_name: list[str]|None=None,
            classes_names: list[str]|None=None,
            childs_classes_names: list[str]|None=None,
            background_image: str|Surface|None=None) -> None:
        """
        A button who display a text and who can be clicked.
        If 'on_click_function' is given, the function will be called on click.
        """
        self._on_click_function = on_click_function
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('button')
        super().__init__(
            ui_manager,
            x,
            y,
            width,
            height,
            anchor,
            visible,
            parent,
            theme_elements_name,
            classes_names,
            childs_classes_names=childs_classes_names,
            background_image=background_image
        )
        self.clickable = True
    
    def update(self) -> None:
        if self.clickable and self._unclicked and self._on_click_function is not None:
            self._on_click_function(self)
        super().update()

    def __copy__(self) -> "Button":
        button_copy = Button(self._ui_manager, self._on_click_function, *self._first_coords, *self._first_size, self.anchor, self._visible, None, self.theme_elements_name, self.classes_names, background_image=self.background_image)
        button_copy.clickable = self.clickable
        button_copy._elements = [copy(element) for element in self._elements]
        for element in button_copy._elements:
            element.parent = button_copy
        button_copy.update_element()
        return button_copy