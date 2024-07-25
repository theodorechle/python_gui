from ui_element import UIElement
from ui_element_interface import UIElementInterface
from ui_manager_interface import UIManagerInterface

class ItemList(UIElement):
    def __init__(self, ui_manager: UIManagerInterface, start_x: int | None = None, start_y: int | None = None, width: int | None = None, height: int | None = None, horizontal_center: bool = False, vertical_center: bool = False, visible: bool = True, parent: UIElementInterface | None = None, theme_elements_name: list[str] = None) -> None:
        super().__init__(ui_manager, start_x, start_y, width, height, horizontal_center, vertical_center, visible, parent, theme_elements_name)