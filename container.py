from ui_element import UIElement
from ui_manager_interface import UIManagerInterface

class Container(UIElement):
    def __init__(self, ui_manager: UIManagerInterface, x: int = 0, y: int = 0, width: int | None = None, height: int | None = None, anchor: str = 'top-left', visible: bool = True, parent: UIElement | None = None, theme_elements_name: list[str] | None = None, class_name: str|None=None) -> None:
        self._elements: list[UIElement] = []
        super().__init__(ui_manager, x, y, width, height, anchor, visible, parent, theme_elements_name, class_name)
    
    def add_element(self, element: UIElement) -> None:
        self._elements.append(element)
        element.parent = self
        self.update_element()
    
    def remove_element(self, element: UIElement) -> None:
        try:
            self._elements.remove(element)
            self._ui_manager.remove_element(element)
            self.update_element()
            self._ui_manager.ask_refresh()
        except ValueError:
            pass
    
    def clear_elements_list(self) -> None:
        for element in self._elements:
            self._ui_manager.remove_element(element)
        self._elements.clear()
        self.update_element()
        self._ui_manager.ask_refresh()

    def get_content_size(self) -> tuple[int, int]:
        max_width, max_height = 0, 0
        for element in self._elements:
            width, height = element.get_size()
            max_width = max(max_width, width)
            max_height = max(max_height, height)
        return (max_width, max_height)

    def update_element(self) -> None:
        super().update_element()
        for element in self._elements:
            element.update_element()