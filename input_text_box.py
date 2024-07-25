from ui_element import UIElement
from ui_element_interface import UIElementInterface
from ui_manager_interface import UIManagerInterface

class InputTextBox(UIElement):
    def __init__(self, ui_manager: UIManagerInterface, text: str="", placeholder_text: str="", forbidden_chars: list[str]|None=None, allowed_chars: list[str]|None=None, start_x: int|None=None, start_y: int|None=None, width: int|None=None, height: int|None=None, horizontal_center: bool=False, vertical_center: bool=False, visible: bool=True, parent: UIElement|None=None, theme_elements_name: list[str]|None=None) -> None:
        """
        A text box made for input usage.
        """
        self._text = text
        self._placeholder_text = placeholder_text
        self.forbidden_chars = forbidden_chars
        self.allowed_chars = allowed_chars
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('input-text-box')
        super().__init__(ui_manager, start_x, start_y, width, height, horizontal_center, vertical_center, visible, parent, theme_elements_name)
        