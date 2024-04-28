import pygame
import pygame_gui
from pygame_gui import UIManager

from PIL import Image

from src.Robot import Robot


def createImageBG(image, viewport_size):
    resized = image.resize(viewport_size)

    bg = pygame.image.fromstring(resized.tobytes(), resized.size, resized.mode)

    return bg


pygame.init()

WIDTH = 1500

background_image = Image.open("./assets/field-masterpiece.png")

viewport_size = (
    int(WIDTH),
    int(WIDTH * background_image.size[1] / background_image.size[0]),
)

win = pygame.display.set_mode(viewport_size)
pygame.display.set_caption("FLL Path Gen")

robot = Robot("./src/constants/robot_constants.json", "./assets/fll_robot.png")

ui_manager = UIManager(viewport_size)

slider_position = (200, 200)
slider_dimensions = (200, 20)
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(slider_position, slider_dimensions),
    start_value=0.2,
    value_range=(0.0, 1.0),
    manager=ui_manager,
)

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        ui_manager.process_events(event)

    win.blit(createImageBG(background_image, win.get_size()), (0, 0))
    win.blit(robot.get_preview(), (0, 0))

    ui_manager.update(clock.tick(60) / 1000.0)

    ui_manager.draw_ui(win)

    print(slider.get_current_value())

    pygame.display.update()

pygame.quit()
