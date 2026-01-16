
from typing import Any

import pygame
from pygame import Vector2

from . import world_globals
from .edit_tool import EditTool, SelectTool, ToolController, HandTool
from .transformation import Transformation
from .viewport import Viewport
from .draw_utils import draw_axis, draw_grid
from .element import Element, Database

class WorldCanvas:
    def __init__(self):
        self.win: pygame.Surface = None
        self.clock = pygame.time.Clock()

        self.database = Database()
        self.world_transform = Transformation(Vector2())

        self.viewport = Viewport(self.world_transform, self.database)

        self.tool_controller: ToolController = ToolController(self.viewport, SelectTool())


    def initialize(self, width, height):
        world_globals.initialize(width, height)
        pygame.init()
        self.win = pygame.display.set_mode((world_globals.win_width, world_globals.win_height))
        pygame.display.set_caption("Map")

    def add_element(self, element: Element) -> None:
        self.database.elements.append(element)

    def handle_event(self, event) -> None:
        self.tool_controller.handle_event(event)

    def step(self) -> None:
        self.tool_controller.step()
        self.viewport.step()

    def draw(self) -> None:
        self.win.fill((30, 30, 30))

        draw_grid(self.win, self.world_transform)
        draw_axis(self.win, self.world_transform)

        for element in self.database.elements:
            element.draw(self.win, self.world_transform)

        self.tool_controller.draw(self.win, self.world_transform)
        self.viewport.draw(self.win, self.world_transform)

    def main_loop(self):
        done = False
        while not done:
            for event in pygame.event.get():
                self.handle_event(event)
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True

            self.step()
            self.draw()

            pygame.display.flip()
            self.clock.tick(world_globals.FPS)
        pygame.quit()


def main():
    context = WorldCanvas()
    context.initialize()
    context.main_loop()


if __name__ == '__main__':
    main()
