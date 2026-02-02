
import pygame


from .viewport import Viewport
from .tool_rule_engine import ToolRule, RuleContext
from .edit_tool import ToolController, HandTool, DragHandleTool



class DragEmptyCanvasRule(ToolRule):
    def matches(self, context: RuleContext, event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            # and context.hovered_element is None
            and context.viewport.get_hovered_handle() is None
        )

    def execute(self, context: RuleContext, event) -> bool:
        context.tool_controller.push_tool(HandTool())
        return True



class MouseUpPopRule(ToolRule):
    def matches(self, context: RuleContext, event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONUP
            and event.button == 1
        )

    def execute(self, context: RuleContext, event) -> bool:
        context.tool_controller.pop_tool()
        return True



class KeyboardZoomRule(ToolRule):
    def __init__(self, key_code: int, **kwargs):
        super().__init__(**kwargs)
        self.key_code = key_code
        self.active = False

    def matches(self, context: RuleContext, event) -> bool:
        return event.type == pygame.MOUSEWHEEL and (pygame.key.get_mods() & pygame.KMOD_ALT)

    def execute(self, context: RuleContext, event) -> bool:
        context.viewport.zoom_by_point(event.y)
        return True



class WheelPanRule(ToolRule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = False

    def matches(self, context: RuleContext, event) -> bool:
        return event.type == pygame.MOUSEWHEEL
    
    def execute(self, context: RuleContext, event) -> bool:
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            context.viewport.pan(False, -event.y)
        else:
            context.viewport.pan(True, -event.y)
        return True



class KeyboardPanRule(ToolRule):
    def __init__(self, key_code: int, **kwargs):
        super().__init__(**kwargs)
        self.key_code = key_code
        self.active = False

    def matches(self, context: RuleContext, event) -> bool:
        return event.type == pygame.KEYDOWN and event.key == self.key_code

    def execute(self, context: RuleContext, event) -> bool:
        context.tool_controller.push_tool(HandTool())
        return True



class KeyboardReleasePopRule(ToolRule):
    def __init__(self, key_code: int, **kwargs):
        super().__init__(**kwargs)
        self.key_code = key_code
        self.active = False

    def matches(self, context: RuleContext, event) -> bool:
        return event.type == pygame.KEYUP and event.key == self.key_code

    def execute(self, context: RuleContext, event) -> bool:
        context.tool_controller.pop_tool()
        return True



class DragHandleRule(ToolRule):
    def matches(self, context: RuleContext, event) -> bool:
        return (
            context.tool_controller.is_idle()
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and context.viewport.get_hovered_handle() is not None
        )

    def execute(self, context: RuleContext, event) -> bool:
        context.tool_controller.push_tool(DragHandleTool(context.viewport))
        return True
