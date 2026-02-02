
from typing import Protocol
from enum import Enum
from dataclasses import dataclass

import pygame
from pygame import Vector2

from .transformation import Transformation
from .viewport import Viewport
from .handle import HandleBase

'''
tools are stateless. do one thing.
'''

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
    '''
    tool applier
    '''
    def __init__(self, context: Viewport, default_tool: EditTool):
        self.context = context
        self.default_tool = default_tool
        self.current_tool = default_tool
        self.stack: list[EditTool] = []

    def is_idle(self) -> bool:
        return self.current_tool == self.default_tool

    def set_tool(self, tool: EditTool):
        self.current_tool.on_deactivate(self.context)
        self.current_tool = tool
        tool.on_activate(self.context)

    def push_tool(self, tool):
        self.stack.append(self.current_tool)
        self.set_tool(tool)
        print(f'current tool: {self.current_tool}')

    def pop_tool(self):
        self.set_tool(self.stack.pop())
        print(f'current tool: {self.current_tool}')

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



@dataclass
class RuleContext:
    viewport: Viewport
    tool_controller: ToolController



class SelectTool(EditTool):
    """Default tool state for hovering and detection handles"""

    def handle_mouse_down(self, context: Viewport, event) -> None:
        """Determines next tool based on what was clicked"""
        ...

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        ...
        # if self.mode == SelectToolMode.HANDLE and self.hovered:
        #     self.hovered.draw(win, transform)



class DragHandleTool(EditTool):
    """Handles dragging of single or multiple handles"""
    def __init__(self, context: Viewport):
        super().__init__()
        self.handle = context.get_hovered_handle()
        mouse_pos = context.world_transform.transform_back(Transformation(Vector2(pygame.mouse.get_pos())))
        self.drag_offset = mouse_pos.pos - self.handle.transformation.pos

    def handle_mouse_motion(self, context: Viewport, event):
        """Updates positions maintaining relative offsets"""
        pos = context.world_transform.transform_back(Transformation(Vector2(event.pos))).pos

        self.handle.set_pos(Vector2(pos - self.drag_offset))
        return self

    def handle_mouse_up(self, context: Viewport, event):
        """Completes drag and returns to idle"""
        ...

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        self.handle.draw(win, transform)


class HandTool(EditTool):
    """Handles canvas panning"""

    def __init__(self):
        super().__init__()
        self.panning = False

    def handle_mouse_down(self, context: Viewport, event) -> 'EditTool':
        """start panning"""
        self.panning = True

    def handle_mouse_motion(self, context: Viewport, event):
        """Pans the canvas"""
        if self.panning:
            context.world_transform.pos -= Vector2(event.rel) * 1 / context.world_transform.scale

    def handle_mouse_up(self, context: Viewport, event):
        """stop panning"""
        self.panning = False


