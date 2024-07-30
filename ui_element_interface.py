from abc import abstractmethod, ABCMeta
from typing import Any

from pygame.event import Event

class UIElementInterface(metaclass=ABCMeta):

    @abstractmethod
    def update_element(self) -> None:
        pass

    @abstractmethod
    def update_theme(self, theme_dict: dict[str, Any], erase=False) -> None:
        """If erase is False, only the changed and added values will be set"""

    @abstractmethod
    def update_start_coords(self) -> None:
        pass

    @abstractmethod
    def get_start_coords(self) -> tuple[int, int]:
        pass
    
    @abstractmethod
    def update_size(self) -> None:
        ...

    @abstractmethod
    def get_content_size(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def get_size(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def is_in_element(self, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def get_visibility(self) -> bool:
        pass
    
    @abstractmethod
    def set_visibility(self, visible: bool) -> None:
        pass

    @abstractmethod
    def toggle_visibility(self) -> bool:
        """Returns True if visible else False"""

    @abstractmethod
    def display_element(self) -> bool:
        """Check whether the element can be displayed before calling the display method"""
    
    @abstractmethod
    def display(self) -> None:
        """Should not be called directly but using display_element method"""
    
    @abstractmethod
    def update(self) -> None:
        """
        Should be called by the subclasses to update the values linked to an event
        (hovered, clicked, ...)
        """
    
    @abstractmethod
    def get_theme_value(self, variable: str) -> Any|None:
        pass

    @abstractmethod
    def display_borders(self) -> None:
        pass

    @abstractmethod
    def process_event(self, event: Event) -> None:
        """
        If the element have the focus and the event can't be processed by the ui manager,
        the element will receive the events in order to process them.
        """