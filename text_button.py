from button import Button
from ui_manager_interface import UIManagerInterface
from typing import Callable
from ui_element import UIElement
from label import Label

class TextButton(Button):
    def __init__(self, ui_manager: UIManagerInterface, text: str, on_click_function: Callable[[Button], None] | None = None, x: int | str = 0, y: int | str = 0, width: int | str | None = None, height: int | str | None = None, anchor: str = 'top-left', visible: bool = True, parent: UIElement | None = None, theme_elements_name: list[str] | None = None, classes_names: list[str] | None = None, background_image: str | None = None) -> None:
        super().__init__(ui_manager, on_click_function, x, y, width, height, anchor, visible, parent, theme_elements_name, classes_names, background_image)
        self.label = Label(self._ui_manager, text, parent=self)
        self.add_element(self.label)
        self.label.fill_parent_width = True
        self.label.fill_parent_height = True
        self.update_element()
    
    def get_text(self) -> str:
        return self.label.get_text()

    def set_text(self, text: str) -> None:
        self.label.set_text(text)
    
