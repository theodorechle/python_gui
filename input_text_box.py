from ui_element import UIElement
from ui_manager import UIManager
from label import Label

import pygame

class InputTextBox(Label):
    def __init__(self, ui_manager: UIManager, text: str="", placeholder_text: str="", forbidden_chars: list[str]|None=None, allowed_chars: list[str]|None=None, loose_focus_on_enter: bool=False, start_x: int|None=None, start_y: int|None=None, width: int|None=None, height: int|None=None, min_width: int=0, min_height: int=0, horizontal_center: bool=False, vertical_center: bool=False, visible: bool=True, parent: UIElement|None=None, theme_elements_name: list[str]|None=None) -> None:
        """
        A text box made for input usage.
        """
        self._placeholder_text = placeholder_text
        self.forbidden_chars = forbidden_chars
        self.allowed_chars = allowed_chars
        if theme_elements_name is None:
            theme_elements_name = []
        theme_elements_name.append('input-text-box')
        self.normal_text = text
        self.placeholder_text = placeholder_text
        self.composition_text = ""
        self.loose_focus_on_enter = loose_focus_on_enter
        self.min_width = min_width
        self.min_height = min_height
        super().__init__(ui_manager, text, start_x, start_y, width, height, horizontal_center, vertical_center, visible, parent, theme_elements_name)
        self.can_have_focus = True
        self.was_focused = False
    
    def update(self) -> None:
        if self.focus and not self.was_focused:
            self.was_focused = True
            pygame.key.start_text_input()
            pygame.key.set_text_input_rect(pygame.Rect(self.get_start_coords(), self.get_size()))
        if not self.focus and self.was_focused:
            pygame.key.stop_text_input()
            self.was_focused = False
        return super().update()
    
    def update_size(self) -> None:
        width, height = self._size
        if self._relative_width or self._relative_height:
            content_width, content_height = self.get_content_size()
        if self._relative_width:
            width = content_width
        if self._relative_height:
            height = content_height
        width += 2*self.get_theme_value('edges-width')
        height += 2*self.get_theme_value('edges-width')
        if width < self.min_width:
            width = self.min_width
        if height < self.min_height:
            height = self.min_height
        self._size = (width, height)

    def update_element(self) -> None:
        self._text = self.normal_text + self.composition_text
        if not self._text:
            self._text = self.placeholder_text
        return super().update_element()

    def process_event(self, event: pygame.event.Event) -> None:
        modified = False
        if event.type == pygame.TEXTINPUT:
            self.normal_text += event.text
            modified = True
        elif event.type == pygame.TEXTEDITING:
            self.composition_text = event.text
            modified = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._ui_manager.set_focus(False)
            elif event.key == pygame.K_BACKSPACE:
                if self.composition_text:
                    self.composition_text = self.composition_text[:-1]
                else:
                    self.normal_text = self.normal_text[:-1]
                modified = True
            elif event.key == pygame.K_RETURN:
                if self.loose_focus_on_enter:
                    self._ui_manager.set_focus(None)
        if modified:
            self.update_element()
            self._ui_manager.ask_refresh()
        
    def get_text(self) -> str:
        return self._text