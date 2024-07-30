from ui_element import UIElement
from ui_manager_interface import UIManagerInterface
from button import Button

class ItemList(UIElement):
    DEFAULT_ELEMENT_HEIGHT = 50
    DEFAULT_ELEMENT_LENGTH = 100
    def __init__(self, ui_manager: UIManagerInterface, elements_height: int|None=None, x: int | str = 0, y: int | str = 0, width: int | str | None = None, height: int | str | None = None, anchor: str = 'top-left', visible: bool = True, parent: UIElement | None = None, theme_elements_name: list[str] | None = None, classes_names: list[str] | None = None, childs_classes_names: list[str]|None=None) -> None:
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('item-list')
        self.elements_height = elements_height if elements_height is not None else self.DEFAULT_ELEMENT_HEIGHT
        self._elements: list[Button] = []
        super().__init__(ui_manager, x, y, width, height, anchor, visible, parent, theme_elements_name, classes_names)
        self.child_focused: Button|None = None
        self.childs_classes_names = childs_classes_names
    
    def add_element(self, text: str='') -> None:
        self._elements.append(Button(
            self._ui_manager,
            text,
            on_click_function=self.set_focus_on_child,
            y=len(self._elements) * self.elements_height,
            width=self._size[0],
            height=self.elements_height + 2*self.border_width,
            classes_names=self.childs_classes_names
            )
        )
        self._elements[-1].can_have_focus = True
        self._elements[-1].parent = self
        self._ui_manager.ask_refresh()
        self.update_element()
    
    def set_focus_on_child(self, element: UIElement) -> None:
        if self.child_focused is not None:
            self.child_focused.set_focus(False)
        self.child_focused = element
        self.child_focused.set_focus(True)

    def get_focused_value(self) -> str|None:
        if self.child_focused is None:
            return
        return self.child_focused.get_text()

    def get_content_size(self) -> tuple[int, int]:
        return (self._size[0] - 2*self.border_width if self._size[0] is not None else self.DEFAULT_ELEMENT_LENGTH, self.elements_height * len(self._elements))

    def update_element(self) -> None:
        super().update_element()
        for element in self._elements:
            element.update_element()