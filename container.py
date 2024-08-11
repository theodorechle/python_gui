from ui_element import UIElement
from ui_manager_interface import UIManagerInterface
from pygame import Surface

class Container(UIElement):
    def __init__(
            self,
            ui_manager: UIManagerInterface,
            x: int = 0,
            y: int = 0,
            width: int | None = None,
            height: int | None = None,
            anchor: str = 'top-left',
            visible: bool = True,
            parent: UIElement | None = None,
            theme_elements_name: list[str] | None = None,
            classes_names: list[str]|None=None,
            childs_classes_names: list[str]|None=None,
            background_image: str|Surface|None=None) -> None:

        self._elements: list[UIElement] = []
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
        """
        Childs elements can get a theme by using
        ':<parent-element-class>:child'
        or
        '<parent-element-name>:child'
        """
        self.childs_classes_names = [] if childs_classes_names is None else childs_classes_names
    
    def add_element(self, element: UIElement) -> UIElement:
        self._elements.append(element)
        element.classes_names.extend(self.childs_classes_names)
        element.parent = self
        self._ui_manager.update_element_theme(element, True)
        self._ui_manager.ask_refresh()
        if self.parent is not None:
            self.parent.update_element()
        else:
            self.update_element()
        return element
    
    def remove_element(self, element: UIElement) -> None:
        try:
            for class_name in self.childs_classes_names:
                try:
                    element.classes_names.remove(class_name)
                except ValueError:
                    pass
            element.parent = None
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
    
    def display(self) -> None:
        super().display()
        for element in self._elements:
            element.display()

    def set_selected(self, selected: bool) -> None:
        for child in self._elements:
            child.set_selected(selected)
        super().set_selected(selected)
