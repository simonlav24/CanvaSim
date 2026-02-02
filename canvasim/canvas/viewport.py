


import pygame
from pygame import Vector2

from .transformation import Transformation
from .element import Element, Database
from .handle import HandleBase


class Viewport:
    def __init__(self, world_transform: Transformation, database: Database):
        self.world_transform = world_transform
        self.database = database
        self.selected_elements: list[Element] = []

        self.hovered_handle: HandleBase = None
        # self.hovered_element: Element = None

    def zoom_by_point(self, amount: float) -> None:
        mouse_pos = Vector2(pygame.mouse.get_pos())
        # Convert mouse position to world coordinates before zoom
        world_pos = self.world_transform.pos + mouse_pos / self.world_transform.scale
        
        # Apply zoom
        if amount > 0:
            self.world_transform.scale *= 1.1
        else:
            self.world_transform.scale *= 0.9
        
        # Adjust position so the world point stays under the mouse
        self.world_transform.pos = world_pos - mouse_pos / self.world_transform.scale

    def pan(self, is_vertical: bool, amount: float) -> None:
        direction = 1 if is_vertical else 0
        self.world_transform.pos[direction] += amount * 50 / self.world_transform.scale

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered_handle = None
            self.hovered_handle = self.get_handle_at(
                self.world_transform.transform_back(Transformation(Vector2(event.pos))).pos)

    def get_handle_at(self, world_pos: Vector2) -> HandleBase:
        for element in reversed(self.database.elements):
            for handle in element.handles:
                if handle.hit_test(world_pos):
                    return handle
        return None
    
    def get_hovered_handle(self) -> HandleBase:
        return self.hovered_handle

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        ...
        # if self.hovered_handle:
        #     self.hovered_handle.draw(win, transform)
