

from random import randint, choice
import sys
from pathlib import Path

# Add parent directory to path so we can import canvasim
sys.path.insert(0, str(Path(__file__).parent.parent))

import pygame
from pygame import Vector2


from canvasim import WorldCanvas
from canvasim import RectanglarSurfElement, TokenElement
from canvasim import Polygon, PolygonTool, Rectangle

from canvasim.canvas.tool_rules import MouseUpPopRule, DragEmptyCanvasRule, KeyboardZoomRule

from canvasim.canvas.tool_rule_engine import ToolRule, ToolRuleEngine


image_background = r'../../dnd-vtt/assets/images/background.png'
image_token = r'../../dnd-vtt/assets/tokens/Token-Character-Monk-Male.png'

def main():
    context = WorldCanvas()
    width, height = 1280, 720
    context.initialize(width, height)

    elements = [
        RectanglarSurfElement(pygame.image.load(image_background)),
    ]

    for _ in range(10):
        elements.append(token := TokenElement(pygame.image.load(image_token)))
        token.transformation.pos = Vector2(randint(0, width), randint(0, height))

    elements.append(Polygon((255, 255, 255), [
        Vector2(0, 0),
        Vector2(0, 100),
        Vector2(200, 100),
    ]))
    elements.append(Rectangle((255, 255, 255), Vector2(100, 100), Vector2(200, 400)))
    [context.add_element(element) for element in elements]

    context.main_loop()


if __name__ == '__main__':
    main()