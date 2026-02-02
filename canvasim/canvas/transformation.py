
from dataclasses import dataclass

from pygame import Vector2


@dataclass
class Transformation:
    pos: Vector2
    scale: float = 1.0

    def transform(self, transformation: 'Transformation') -> 'Transformation':
        return Transformation((transformation.pos - self.pos) * self.scale, self.scale * transformation.scale)
    
    def transform_back(self, transformation: 'Transformation') -> 'Transformation':
        return Transformation(transformation.pos / self.scale + self.pos, transformation.scale / self.scale)
    
    def set_pos(self, new_pos: Vector2) -> None:
        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]
