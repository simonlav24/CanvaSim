

import pygame

from .viewport import Viewport
from .edit_tool import ToolController


class ToolRule:
    def __init__(self, **kwargs):
        self.priority = kwargs.get('priority', 0)
    
    def matches(self, context: Viewport, event) -> bool:
        raise NotImplementedError

    def execute(self, controller: ToolController, context: Viewport, event) -> bool:
        raise NotImplementedError



class ToolRuleEngine:
    '''tool changing'''
    def __init__(self, context: Viewport, tool_controller:ToolController):
        self.context = context
        self.tool_controller = tool_controller
        self.rules: list[ToolRule] = []

    def add_rule(self, rule: ToolRule):
        self.rules.append(rule)

    def handle_event(self, event):
        for rule in sorted(self.rules, key=lambda r: r.priority, reverse=True):
            if rule.matches(self.context, event):
                print(f'rule matched: {rule}')
                consumed = rule.execute(self.tool_controller, self.context, event)
                if consumed:
                    return





