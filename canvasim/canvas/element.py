
from dataclasses import dataclass, field
from typing import Any

import pygame
from pygame import Vector2

from .transformation import Transformation
from . import world_globals
from .handle import HandleBase, PointHandle



class Element:
    def __init__(self):
        self.transformation = Transformation(Vector2())
        self.handles: list[HandleBase] = []
    
    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        ...

    def hit_test(self, world_pos: Vector2) -> bool:
        ...

    def set_pos(self, pos: Vector2) -> None:
        self.transformation.pos[0] = pos[0]
        self.transformation.pos[1] = pos[1]
    
    def get_pos(self) -> Vector2:
        return self.transformation.pos



@dataclass
class Database:
    elements: list[Element] = field(default_factory=list)


class TokenElement(Element):
    def __init__(self, surf: pygame.Surface):
        super().__init__()
        self.surf = surf
        self.handles.append(PointHandle(self.transformation, max(*self.surf.get_size()) / 2, self))
    
    def hit_test(self, world_pos):
        return self.handles[0].hit_test(world_pos)

    def draw(self, win: pygame.Surface, world_transform: Transformation) -> None:
        # Combine element's transform with world transform
        screen_transform = world_transform.transform(self.transformation)
        
        # Calculate scaled size
        surf_width, surf_height = self.surf.get_size()
        scaled_width = int(surf_width * screen_transform.scale)
        scaled_height = int(surf_height * screen_transform.scale)
        
        if scaled_width <= 0 or scaled_height <= 0:
            return
        
        # Scale the surface
        scaled_surf = pygame.transform.scale(self.surf, (scaled_width, scaled_height))
        
        # Draw centered on the position
        draw_pos = screen_transform.pos - Vector2(scaled_width / 2, scaled_height / 2)
        
        win.blit(scaled_surf, draw_pos)
        # for handle in self.handles:
        #     handle.draw(win, world_transform)


