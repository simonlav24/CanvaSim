

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
from canvasim import GuiContext, Label, Button, ToggleButton


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


    # gui
    gui_context = GuiContext()
    gui_context.set_layout([
        [Label('label1:'), Button('button1', key='button1')],
        [Label('label2:'), Button('button2', key='button2')],
        [Label('label3:'), Button('button3', key='button3')],
        [Label('label3:'), ToggleButton('selected', key='button3')],
    ])

    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():
            event_handled = False
            gui_context.handle_event(event)
            for event in gui_context.get_gui_events():
                event_handled = True
                print(f'GUI Event: {event.type}, Data: {event.data}')
            if event_handled:
                continue

            context.handle_event(event)

            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        
        context.step()
        gui_context.step()
        
        context.draw()
        gui_context.draw(context.win)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()