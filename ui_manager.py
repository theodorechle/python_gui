import pygame
from ui_element_interface import UIElementInterface
from ui_manager_interface import UIManagerInterface

from json import load, JSONDecodeError
from typing import Any
import os

ELEMENT_HOVERED = pygame.event.custom_type()
ELEMENT_CLICKED = pygame.event.custom_type()
ELEMENT_UNCLICKED = pygame.event.custom_type()
ELEMENT_WHEEL_MOVED = pygame.event.custom_type()

class UIManager(UIManagerInterface):
    def __init__(self, window: pygame.Surface) -> None:
        self.window: pygame.Surface = window
        self._elements: list[UIElementInterface] = []
        self._elements_to_display: list[UIElementInterface] = []
        self._refresh_all = False
        self._focused_element: UIElementInterface|None = None
        self._theme = self.get_theme(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_theme.json'))
        if not self._theme:
            raise FileNotFoundError("Can't find default theme file or file is not valid json")

    def get_theme(self, path: str) -> dict[str, Any]:
        try:
            with open(path) as f:
                return load(f)
        except (FileNotFoundError, JSONDecodeError):
            print(f"Path '{path}' not found")
            return {}
    
    def _update_elements_themes(self, theme: dict[str,dict[str,Any]]) -> None:
        for element_theme in theme:
            if element_theme in self._theme:
                self._theme[element_theme].update(theme[element_theme])
            else:
                self._theme[element_theme] = theme[element_theme]

    def update_theme(self, path: str|None=None, theme_dict: dict[str, Any]|None=None, erase: bool=False) -> None:
        if erase:
            self._theme.clear()
        changed = False
        if path is not None:
            changed = True
            self._update_elements_themes(self.get_theme(path))
        if theme_dict is not None:
            changed = True
            self._update_elements_themes(theme_dict)
        if changed:
            for element in self._elements:
                element.update_theme(self._theme, erase)
                element.update_element()
            self.ask_refresh()

    def get_window_size(self) -> tuple[int, int]:
        return self.window.get_size()

    def get_window(self) -> pygame.Surface:
        return self.window

    def add_element(self, element: UIElementInterface) -> None:
        self._elements.append(element)
        element.update_theme(self._theme)
        self.ask_refresh()
    
    def remove_element(self, element: UIElementInterface) -> None:
        try:
            self._elements.remove(element)
            self.ask_refresh()
        except ValueError:
            pass

    def clear_elements_list(self) -> None:
        self._elements.clear()
        self._elements_to_display.clear()
        self.ask_refresh()

    def ask_refresh(self, element: UIElementInterface|list[UIElementInterface]|None=None) -> None:
        """
        Ask the UIManager to re-display the window the next time it will be called for an update.
        If an element is given, it will only re-display the element.

        Note: If an element or a list of element is given, it will display it without caring of a size change, 
        so it should be given only if the starting coords and the size are the same as at the last refresh.
        """
        if element is None:
            self._refresh_all = True
            return
        if isinstance(element, UIElementInterface):
            if element in self._elements_to_display: return
            self._elements_to_display.append(element)
        else:
            for e in element:
                if e in self._elements_to_display: continue
                self._elements_to_display.append(e)

    def display(self) -> None:
        if self._refresh_all:
            self.window.fill("#000000")
            elements = self._elements
        else:
            elements = self._elements_to_display
        for element in elements:
            if not self._refresh_all:
                element.clear = True
            element.display_element()
        self._refresh_all = False
        self._elements_to_display.clear()
    
    def get_hovered_element(self) -> list[UIElementInterface]:
        x, y = pygame.mouse.get_pos()
        return [element for element in self._elements if element.is_in_element(x, y)]

    def set_focus(self, element: UIElementInterface|None) -> None:
        if self._focused_element is not None:
            self._focused_element.set_focus(False)
        self._focused_element = element
        if element is not None:
            element.set_focus(True)
    
    def get_focus(self) -> UIElementInterface|None:
        return self._focused_element

    def process_event(self, event: pygame.event.Event) -> None:
        """
        Try to process the given events.
        If the event is not MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP or MOUSEWHEEL,
        if an element have the focus, the event will be sent to the focused element
        """
        if event.type == pygame.MOUSEMOTION:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5): return # wheel
            elements = self.get_hovered_element()
            for element in elements:
                element.clicked = True
                pygame.event.post(pygame.event.Event(ELEMENT_CLICKED, dict={'element': element}))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button in (4, 5): return # wheel
            elements = self.get_hovered_element()
            is_focused = False
            for element in elements:
                element.unclicked = True
                if not is_focused and element.can_have_focus:
                    is_focused = True
                    if self.get_focus() != element:
                        self.set_focus(element)
                pygame.event.post(pygame.event.Event(ELEMENT_UNCLICKED, dict={'element': element}))
            if not is_focused:
                self.set_focus(None)
        elif event.type == pygame.MOUSEWHEEL:
            x, y = event.x, event.y
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                x, y = y, x
            elements = self.get_hovered_element()
            for element in elements:
                element.wheel_move = x, y
                pygame.event.post(pygame.event.Event(ELEMENT_WHEEL_MOVED, dict={'element': element}))
        elif self._focused_element is not None:
            self._focused_element.process_event(event)


    def update(self) -> None:
        """Refresh the window if needed and creates events (click, hover)"""

        elements = self.get_hovered_element()
        for element in elements:
            element.hovered = True
            pygame.event.post(pygame.event.Event(ELEMENT_HOVERED, dict={'element': element}))
        self.display()
        for element in self._elements:
            element.update()
