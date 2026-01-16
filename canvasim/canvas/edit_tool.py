
from typing import Protocol
from enum import Enum

import pygame
from pygame import Vector2

from .transformation import Transformation
from .viewport import Viewport
from .handle import Selectable



class EditTool:
    """Base class for editor tools using State pattern"""
    def __init__(self):
        ...

    def handle_mouse_down(self, context: Viewport, event) -> None:
        """Handles mouse button down event"""

    def handle_mouse_up(self, context: Viewport, event) -> None:
        """Handles mouse button up event"""

    def handle_mouse_motion(self, context: Viewport, event) -> None:
        """Handles mouse motion event"""

    def handle_key_down(self, context: Viewport, event) -> None:
        """Handles key down event"""

    def handle_key_up(self, context: Viewport, event) -> None:
        """Handles key up event"""

    def handle_mouse_scroll(self, context: Viewport, event) -> None:
        """Handles key up event"""

    def on_activate(self, context: Viewport) -> None:
        ...
    
    def on_deactivate(self, context: Viewport) -> None:
        ...

    def step(self) -> None:
        """Updates tool state each frame"""
        ...

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        """Draws tool-specific overlays"""
        ...



class ToolController:
    def __init__(self, context: Viewport, default_tool: EditTool):
        self.context = context
        self.current_tool = default_tool
        self.stack: list[EditTool] = []

    def set_tool(self, tool: EditTool):
        self.current_tool.on_deactivate(self.context)
        self.current_tool = tool
        tool.on_activate(self.context)

    def push_tool(self, tool):
        self.stack.append(self.current_tool)
        self.set_tool(tool)

    def pop_tool(self):
        self.set_tool(self.stack.pop())

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.current_tool.handle_mouse_down(self.context, event)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.current_tool.handle_mouse_up(self.context, event)

        if event.type == pygame.MOUSEMOTION:
            self.current_tool.handle_mouse_motion(self.context, event)

        if event.type == pygame.KEYDOWN:
            self.current_tool.handle_key_down(self.context, event)

        if event.type == pygame.KEYUP:
            self.current_tool.handle_key_up(self.context, event)

        if event.type == pygame.MOUSEWHEEL:
            self.current_tool.handle_mouse_scroll(self.context, event)


    def step(self) -> None:
        self.current_tool.step()
    
    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        self.current_tool.draw(win, transform)



class SelectTool(EditTool):
    """Default tool state for hovering and detection handles"""

    def handle_mouse_down(self, context: Viewport, event) -> 'EditTool':
        """Determines next tool based on what was clicked"""
        ...

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        ...
        # if self.mode == SelectToolMode.HANDLE and self.hovered:
        #     self.hovered.draw(win, transform)

    



class DragElementTool(EditTool):
    """Handles dragging of single or multiple handles"""
    def __init__(self, viewport, main_element: Selectable):
        super().__init__(viewport)
        self.main_element = main_element
        mouse_pos = self.viewport.world_transform.transform_back(Transformation(Vector2(pygame.mouse.get_pos())))
        self.drag_offset = mouse_pos.pos - self.main_element.transformation.pos

    def handle_mouse_motion(self, event):
        """Updates positions maintaining relative offsets"""
        pos = self.viewport.world_transform.transform_back(Transformation(Vector2(event.pos))).pos

        self.main_element.transformation.pos = Vector2(pos - self.drag_offset)
        return self

    def handle_mouse_up(self, event):
        """Completes drag and returns to idle"""
        return SelectTool(self.viewport)


class HandTool(EditTool):
    """Handles canvas panning"""

    def handle_mouse_motion(self, context: Viewport, event):
        """Pans the canvas"""
        context.world_transform.pos -= Vector2(event.rel) * 1 / context.world_transform.scale

    def handle_mouse_up(self, context: Viewport, event):
        """stop panning"""


class ZoomTool(EditTool):
    def handle_mouse_scroll(self, context, event):
        context.zoom_by_point(event.y)
