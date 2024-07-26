from ui_manager_interface import UIManagerInterface
import pygame

from typing import Any

class UIElement:
    def __init__(self, ui_manager: UIManagerInterface, x: int=0, y: int=0, width: int|None=None, height: int|None=None, anchor: str='top-left', visible: bool=True, parent: "UIElement|None"=None, theme_elements_name: list[str]|None=None) -> None:
        """
        Params:
        - ui_manager: the manager where will be send events and who keeps informations like window size
        - x: the value who will be added to the x of the element, after the anchor will be set
        - y: the value who will be added to the y of the element, after the anchor will be set
        - width: if not None, set the element width, else set relative size to True for width
        - height: if not None, set the element height, else set relative size to True for height
        - anchor: a string telling where the element will be positioned in his parent.
            Possible anchors: top-left, top, top-right, left, center, right, bottom-left, bottom, bottom-right
            Default is top-left
        - visible: Whether the element should be displayed or not
        - theme_elements_name: a list of the themes' names of the subclasses
        """
        self.theme_elements_name = ['ui-element'] # a list of the class name and all is subclasses to get the themes
        if theme_elements_name is not None:
            self.theme_elements_name.extend(theme_elements_name)
        self._theme = {}
        self.edges_width = 0
        self._ui_manager = ui_manager
        self._ui_manager.add_element(self)
        self._coords = x, y
        self._start_coords = x, y
        self._size = (width, height)
        self._relative_width = width is None
        self._relative_height = height is None
        self.anchor = anchor
        self.parent = parent
        self._visible = visible
        self.hovered = False
        self.clicked = False
        self.was_clicked = False
        self.unclicked = False
        self.wheel_move = (0, 0)
        self.can_have_focus = False
        self.focus = False
        self.update_element()

    def update_element(self) -> None:
        self.update_size()
        self.update_start_coords()

    def update_theme(self, theme_dict: dict[str, Any], erase=False) -> None:
        """If erase is False, only the changed and added values will be set"""
        if erase:
            self._theme.clear()
        for element_name in self.theme_elements_name:
            if element_name in theme_dict:
                self._theme.update(theme_dict[element_name])
        self.edges_width = self.get_theme_value('edges-width')

    def get_start_coords(self) -> None:
        return self._start_coords

    def get_surface_rect(self) -> pygame.Rect:
        return pygame.Rect(self._start_coords, self._size)

    def update_start_coords(self) -> None:
        x, y = 0, 0
        if self.parent is None:
            parent_rect = (0, 0, *self._ui_manager.get_window_size())
        else:
            parent_rect = self.parent.get_surface_rect()
        if self.anchor == 'top-left':
            x = parent_rect[0] + self.edges_width
            y = parent_rect[1] + self.edges_width
        elif self.anchor == 'top':
            x = parent_rect[0] + self.edges_width + parent_rect[2] // 2 - self.get_size()[0] // 2
            y = parent_rect[1] + self.edges_width
        elif self.anchor == 'top-right':
            x = parent_rect[0] + parent_rect[2] - self.get_size()[0] - self.edges_width
            y = parent_rect[1] + self.edges_width
        elif self.anchor == 'center':
            x = parent_rect[0] + self.edges_width + parent_rect[2] // 2 - self.get_size()[0] // 2
            y = parent_rect[1] + self.edges_width + parent_rect[3] // 2 - self.get_size()[1] // 2
        elif self.anchor == 'left':
            x = parent_rect[0] + self.edges_width
            y = parent_rect[1] + self.edges_width + parent_rect[3] // 2 - self.get_size()[1] // 2
        elif self.anchor == 'right':
            x = parent_rect[0] + parent_rect[2] - self.get_size()[0] - self.edges_width
            y = parent_rect[1] + self.edges_width + parent_rect[3] // 2 - self.get_size()[1] // 2
        elif self.anchor == 'bottom-left':
            x = parent_rect[0] + self.edges_width
            y = parent_rect[1] + parent_rect[3] - self.get_size()[1] - self.edges_width
        elif self.anchor == 'bottom':
            x = parent_rect[0] + self.edges_width + parent_rect[2] // 2 - self.get_size()[0] // 2
            y = parent_rect[1] + parent_rect[3] - self.get_size()[1] - self.edges_width
        elif self.anchor == 'bottom-right':
            x = parent_rect[0] + parent_rect[2] - self.get_size()[0] - self.edges_width
            y = parent_rect[1] + parent_rect[3] - self.get_size()[1] - self.edges_width
        x += self._coords[0]
        y += self._coords[1]
        self._start_coords = x, y
    
    def update_size(self) -> None:
        width, height = self._size
        if self._relative_width or self._relative_height:
            content_width, content_height = self.get_content_size()
            content_width += 2*self.edges_width
            content_height += 2*self.edges_width
        if self._relative_width:
            width = content_width
        if self._relative_height:
            height = content_height
        self._size = (width, height)

    def get_content_size(self) -> tuple[int, int]:
        raise NotImplementedError

    def get_size(self) -> tuple[int, int]:
        return self._size

    def is_in_element(self, x: int, y: int) -> bool:
        return self._start_coords[0] <= x <= self._start_coords[0] + self._size[0] and self._start_coords[1] <= y <= self._start_coords[1] + self._size[1]

    def get_visibility(self) -> bool:
        return self._visible
    
    def set_visibility(self, visible: bool) -> None:
        self._visible = visible
        self._ui_manager.ask_refresh()
    
    def toggle_visibility(self) -> bool:
        """Returns True if visible else False"""
        self._visible = not self._visible
        self._ui_manager.ask_refresh()
        return self._visible

    def display_element(self) -> bool:
        """Check whether the element can be displayed before calling the display method"""
        if self._visible:
            self.display()
    
    def display(self) -> None:
        """Should not be called directly but using display_element method"""
        background_color = self.get_theme_value('background-color')
        if background_color is not None:
            pygame.draw.rect(self._ui_manager.window, background_color, pygame.Rect(self.get_start_coords(), self.get_size()))
        self.display_edge()
    
    def update(self) -> None:
        """
        Should be called by the subclasses to update the values linked to an event
        (hovered, clicked, ...)
        """
        if self.clicked and self.get_theme_value('clicked-egdes-color') is not None:
            self._ui_manager.ask_refresh()
        elif self.hovered and self.get_theme_value('hovered-edges-color') is not None:
            self._ui_manager.ask_refresh()
        self.hovered = False
        if self.clicked:
            self.was_clicked = True
        self.clicked = False
        if self.unclicked and self.was_clicked:
            self.was_clicked = False
        self.unclicked = False
        
    def get_theme_value(self, variable: str) -> Any|None:
        return self._theme.get(variable)

    def display_edge(self) -> None:
        edges_color = None
        if self.clicked or self.was_clicked:
            edges_color = self.get_theme_value('clicked-edges-color')
        elif self.hovered:
            edges_color = self.get_theme_value('hovered-edges-color')
        if edges_color is None:
            edges_color = self.get_theme_value('edges-color')
        pygame.draw.rect(
            self._ui_manager.window,
            edges_color,
            pygame.Rect(
                self._start_coords[0],
                self._start_coords[1],
                self._size[0],
                self._size[1]
            ),
            self.edges_width,
            self.get_theme_value('border-radius'),
            self.get_theme_value('border-top-left-radius'),
            self.get_theme_value('border-top-right-radius'),
            self.get_theme_value('border-bottom-left-radius'),
            self.get_theme_value('border-bottom-right-radius')
        )

    def process_event(self, event: pygame.event.Event) -> None:
        """
        If the element have the focus and the event can't be processed by the ui manager,
        the element will receive the events in order to process them.
        """