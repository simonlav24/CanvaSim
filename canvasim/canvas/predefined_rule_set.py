
import pygame

from .edit_tool import HandTool, SelectTool
from .tool_rule_engine import ToolRule
from .tool_rules import *

def editor_tool_set():
    return [
        DragEmptyCanvasRule(),
        MouseUpPopRule(),
        KeyboardZoomRule(pygame.K_LALT, priority=10),
        WheelPanRule(),
    ]
