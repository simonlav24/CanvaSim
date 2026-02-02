
import pygame

from .edit_tool import HandTool, SelectTool
from .tool_rule_engine import ToolRule
from .tool_rules import *


def editor_tool_set_drag_anywhere():
    return [
        DragEmptyCanvasRule(),
        MouseUpPopRule(),
        KeyboardZoomRule(pygame.K_LALT, priority=10),
        WheelPanRule(),
    ]


def editor_tool_set():
    return [
        KeyboardZoomRule(pygame.K_LALT, priority=10), # shall be bigger than WheelPanRule
        WheelPanRule(),
        KeyboardPanRule(pygame.K_SPACE, priority=5),
        KeyboardReleasePopRule(pygame.K_SPACE),
        DragHandleRule(),
        MouseUpPopRule(),
    ]