from ui_element import UIElement
from ui_manager_interface import UIManagerInterface
from text_button import TextButton
from typing import Callable
from pygame import Surface

class Table(UIElement):
    _SIZE_SCROLL_SHIFT = 10
    def __init__(
            self,
            ui_manager: UIManagerInterface,
            nb_elements_width: int,
            nb_elements_height: int,
            elements_width: int|None=None,
            elements_height: int|None=None,
            x: int | str = 0,
            y: int | str = 0,
            width: int | str | None = None,
            height: int | str | None = None,
            anchor: str = 'top-left',
            visible: bool = True,
            parent: UIElement | None = None,
            theme_elements_name: list[str] | None = None,
            classes_names: list[str] | None = None,
            cells_classes_names: list[str]|None=None,
            cells_childs_classes_names: list[str]|None=None,
            on_select_item_function: Callable[[TextButton], None]|None=None,
            background_image: str|Surface|None=None) -> None:
        if theme_elements_name is None:
            theme_elements_name = []
        self.scroll_shift = (0, 0)
        theme_elements_name.append('item-list')
        self.nb_elements_width = nb_elements_width
        self.nb_elements_height = nb_elements_height
        self.elements_width = elements_width if elements_width is not None else 0
        self.elements_height = elements_height if elements_height is not None else 0
        self._elements: list[TextButton] = [None for _ in range(self.nb_elements_width * self.nb_elements_height)]
        self.max_elements_heights = [self.elements_height] * self.nb_elements_height
        self.max_elements_widths = [self.elements_width] * self.nb_elements_width
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
            background_image
        )
        self.child_selected: TextButton|None = None
        self.cells_classes_names = [] if cells_classes_names is None else cells_classes_names
        self.cells_childs_classes_names = [] if cells_childs_classes_names is None else cells_childs_classes_names
        self.on_select_function = on_select_item_function
    
    def add_element(self, text: str, x: int, y: int) -> bool:
        index = x + y * self.nb_elements_width
        if index < 0 or index > len(self._elements): return False
        previous_width = sum(self.max_elements_widths[:x])
        previous_height = sum(self.max_elements_heights[:y])
        new_element = TextButton(
            self._ui_manager,
            text,
            on_click_function=self.set_selected_child,
            x=previous_width, 
            y=previous_height,
            classes_names=self.cells_classes_names.copy(),
            childs_classes_names=self.cells_childs_classes_names,
            parent=self
        )
        self._elements[index] = new_element
        new_element.can_have_focus = True
        self.max_elements_widths[x] = max(self.max_elements_widths[x], new_element._size[0])
        self.max_elements_heights[y] = max(self.max_elements_heights[y], new_element._size[1])
        new_element._relative_width = False
        new_element._relative_height = False
        if self._relative_width:
            self._size = (previous_width + self.max_elements_widths[y], self._size[1])
        if self._relative_height:
            self._size = (self._size[0], previous_height + self.max_elements_heights[y])
        self._ui_manager.ask_refresh()
        self.update_element()
        return True
    
    def remove_element(self, x: int, y: int) -> bool:
        index = x + y * self.nb_elements_width
        if index < 0 or index > len(self._elements): return False
        element = self._elements[index]
        if element is None: return False
        for class_name in self.cells_classes_names:
            try:
                element.classes_names.remove(class_name)
            except ValueError:
                pass
        element.parent = None
        self._elements[index] = None
        if self.child_selected == element:
            self.child_selected = None
        self._ui_manager.remove_element(element)
        self.update_element()
        self._ui_manager.ask_refresh()
        return True

    def set_selected_child(self, element: UIElement) -> None:
        if self.child_selected is not None:
            self.child_selected.set_selected(False)
        self.child_selected = element
        self.child_selected.set_selected(True)
        if self.on_select_function is not None:
            self.on_select_function(self.child_selected)

    def get_focused_value(self) -> str|None:
        if self.child_selected is None:
            return
        return self.child_selected.get_text()

    def get_content_size(self) -> tuple[int, int]:
        width = sum(self.max_elements_widths)
        height = sum(self.max_elements_heights)
        if height != 0:
            height -= 2*self._border_width
        if width != 0:
            width -= 2*self._border_width
        if not self._relative_width:
            width = min(self._size[0], width)
        if not self._relative_height:
            height = min(self._size[1], height)
        
        return width, height

    def update_element(self) -> None:
        super().update_element()
        for index, element in enumerate(self._elements):
            if element is None: continue
            x, y = index % self.nb_elements_width, index // self.nb_elements_width
            element._first_coords = (sum(self.max_elements_widths[:x]) - self._SIZE_SCROLL_SHIFT * self.scroll_shift[0], sum(self.max_elements_heights[:y]) - self._SIZE_SCROLL_SHIFT * self.scroll_shift[1])
            element._first_size = self.max_elements_widths[x], self.max_elements_heights[y]
            element.update_element()
    
    def scroll_elements(self) -> None:
        y = self.wheel_move[1]
        if y >= 0:
            y = min(y, self.scroll_shift[1])
        elif y < 0:
            if self._size[1] >= sum(self.max_elements_heights) - self.scroll_shift[1] * self._SIZE_SCROLL_SHIFT:
                y = 0
        x = self.wheel_move[0]
        if x >= 0:
            x = min(x, self.scroll_shift[0])
        elif x < 0:
            if self._size[0] >= sum(self.max_elements_widths) - self.scroll_shift[0] * self._SIZE_SCROLL_SHIFT:
                x = 0
        if x == 0 and y == 0: return
        self.scroll_shift = self.scroll_shift[0] - x, self.scroll_shift[1] - y
        for element in self._elements:
            if element is None: continue
        self.update_element()
        self._ui_manager.ask_refresh()

    def update(self) -> None:
        if self.wheel_move[0] != 0 or self.wheel_move[1] != 0:
            self.scroll_elements()
        super().update()

    def display(self) -> None:
        super().display()
        for element in self._elements:
            if element is None: continue
            element.display()