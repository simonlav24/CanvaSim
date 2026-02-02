
from typing import Any, Protocol

import pygame
from pygame import Vector2
from .transformation import Transformation



class HandleBase:
    def __init__(self, transformation: Transformation, owner: Any):
        self.transformation = transformation
        self.owner: Any = owner
    
    def hit_test(self, world_pos: Vector2) -> bool:
        ...
    
    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        ...

    def set_pos(self, new_pos: Vector2) -> None:
        self.transformation.set_pos(new_pos)



class PointHandle(HandleBase):
    def __init__(self, transformation: Transformation, owner: Any, radius: float):
        super().__init__(transformation, owner)
        self.radius = radius
    
    def hit_test(self, world_pos: Vector2) -> bool:
        my_world_pos = self.transformation
        if (world_pos - my_world_pos.pos).length() < self.radius:
            return True
        return False
    
    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        my_world_pos = transform.transform(self.transformation)
        pygame.draw.circle(win, (255, 255, 255), my_world_pos.pos, self.radius * transform.scale, 1)

