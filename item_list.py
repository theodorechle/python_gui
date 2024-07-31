from ui_element import UIElement
from ui_manager_interface import UIManagerInterface
from button import Button

class ItemList(UIElement):
    DEFAULT_ELEMENT_HEIGHT = 50
    DEFAULT_ELEMENT_LENGTH = 100
    SCROLL_DISPLACEMENT = 10
    def __init__(self, ui_manager: UIManagerInterface, elements_height: int|None=None, x: int | str = 0, y: int | str = 0, width: int | str | None = None, height: int | str | None = None, anchor: str = 'top-left', visible: bool = True, parent: UIElement | None = None, theme_elements_name: list[str] | None = None, classes_names: list[str] | None = None, childs_classes_names: list[str]|None=None) -> None:
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('item-list')
        self.elements_height = elements_height if elements_height is not None else self.DEFAULT_ELEMENT_HEIGHT
        self._elements: list[Button] = []
        super().__init__(ui_manager, x, y, width, height, anchor, visible, parent, theme_elements_name, classes_names)
        self.child_focused: Button|None = None
        self.childs_classes_names = childs_classes_names
        self.max_child_size = 0
    
    def add_element(self, text: str) -> None:
        self._elements.append(Button(
            self._ui_manager,
            text,
            on_click_function=self.set_focus_on_child,
            y=len(self._elements) * self.elements_height,
            height=self.elements_height,
            classes_names=self.childs_classes_names,
            parent=self
            )
        )
        self._elements[-1].can_have_focus = True
        self._elements[-1].fill_parent = True
        self.max_child_size = max(self.max_child_size, self._elements[-1]._size[0])
        if self._relative_width:
            self._size = (self.max_child_size, self._size[1])
        self._ui_manager.ask_refresh()
        self.update_element()
    
    def add_elements(self, texts: list[str]) -> None:
        for text in texts:
            self._elements.append(Button(
                self._ui_manager,
                text,
                on_click_function=self.set_focus_on_child,
                y=len(self._elements) * self.elements_height,
                height=self.elements_height,
                classes_names=self.childs_classes_names,
                parent=self
                )
            )
            self._elements[-1].can_have_focus = True
            self._elements[-1].fill_parent = True
            self.max_child_size = max(self.max_child_size, self._elements[-1]._size[0])
            if self._relative_width:
                self._size = (self.max_child_size, self._size[1])
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
        width = self._size[0] - 2*self.border_width if self._size[0] is not None else self.DEFAULT_ELEMENT_LENGTH
        height = self.elements_height * len(self._elements)
        if height != 0:
            height -= 2*self.border_width
        if not self._relative_width:
            width = min(self._size[0], width)
        if not self._relative_height:
            height = min(self._size[1], height)
        
        return width, height

    def update_element(self) -> None:
        super().update_element()
        for element in self._elements:
            element._first_size = self.max_child_size, element._first_size[1]
            element._relative_width = False
            element.update_element()
    
    def display(self) -> None:
        super().display()
        for element in self._elements:
            element.display()
    
    def scroll_elements(self) -> None:
        y = self.wheel_move[1]
        if y >= 0:
            y = min(y, (self._start_coords[1] - self._elements[0]._start_coords[1]) // self.SCROLL_DISPLACEMENT)
        if y <= 0:
            y = max(y, (self._start_coords[1] + self._size[1] - self._elements[-1]._start_coords[1] - self.elements_height) // self.SCROLL_DISPLACEMENT)
        x = self.wheel_move[0]
        if x >= 0:
            x = min(x, (self._start_coords[0] - self._elements[0]._start_coords[0]) // self.SCROLL_DISPLACEMENT)
        if x <= 0:
            x = max(x, (self._start_coords[0] + self._size[0] - self._elements[0]._start_coords[0] - self.max_child_size) // self.SCROLL_DISPLACEMENT)
        if x == 0 and y == 0: return
        for element in self._elements:
            element._first_coords = (element._first_coords[0] + self.SCROLL_DISPLACEMENT * x, element._first_coords[1] + self.SCROLL_DISPLACEMENT * y)
        self.update_element()
        self._ui_manager.ask_refresh()

    def update(self) -> None:
        if self.wheel_move[0] != 0 or self.wheel_move[1] != 0:
            self.scroll_elements()
        super().update()