
from dataclasses import dataclass

import pygame

from .viewport import Viewport
from .edit_tool import ToolController, RuleContext



class ToolRule:
    def __init__(self, **kwargs):
        self.priority = kwargs.get('priority', 0)
    
    def matches(self, context: RuleContext, event) -> bool:
        raise NotImplementedError

    def execute(self, context: RuleContext, event) -> bool:
        raise NotImplementedError



class ToolRuleEngine:
    '''tool changing'''
    def __init__(self, viewport: Viewport, tool_controller:ToolController):
        self.context = RuleContext(viewport, tool_controller)
        self.tool_controller = tool_controller
        self.rules: list[ToolRule] = []

    def set_rules(self, rules: list[ToolRule]):
        self.rules = rules

    def handle_event(self, event):
        for rule in sorted(self.rules, key=lambda r: r.priority, reverse=True):
            if rule.matches(self.context, event):
                # print(f'rule matched: {rule}')
                consumed = rule.execute(self.context, event)
                if consumed:
                    return





