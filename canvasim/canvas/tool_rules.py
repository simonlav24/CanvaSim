
import pygame


from .viewport import Viewport
from .tool_rule_engine import ToolRule
from .edit_tool import ToolController, HandTool



class DragEmptyCanvasRule(ToolRule):
    def matches(self, context: Viewport, event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and context.hovered_element is None
            and context.hovered_handle is None
        )

    def execute(self, controller: ToolController, context: Viewport, event) -> bool:
        controller.push_tool(HandTool())
        return True



class MouseUpPopRule(ToolRule):
    def matches(self, context: Viewport, event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONUP
            and event.button == 1
        )

    def execute(self, controller: ToolController, context: Viewport, event) -> bool:
        controller.pop_tool()
        return True



class KeyboardZoomRule(ToolRule):
    def __init__(self, key_code: int, **kwargs):
        super().__init__(**kwargs)
        self.key_code = key_code
        self.active = False

    def matches(self, context: Viewport, event) -> bool:
        return event.type == pygame.MOUSEWHEEL and (pygame.key.get_mods() & pygame.KMOD_ALT)

    def execute(self, controller: ToolController, context: Viewport, event) -> bool:
        context.zoom_by_point(event.y)
        return True



class WheelPanRule(ToolRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = False

    def matches(self, context: Viewport, event) -> bool:
        return event.type == pygame.MOUSEWHEEL
    
    def execute(self, controller: ToolController, context: Viewport, event) -> bool:
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            context.pan(False, -event.y)
        else:
            context.pan(True, -event.y)
        return True
