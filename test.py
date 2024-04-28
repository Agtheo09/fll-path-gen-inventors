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

robot = Robot(
    (200, 20, 30), "./src/constants/robot_constants.json", "./assets/fll_robot.png"
)

ui_manager = UIManager(viewport_size)

slider_position = (200, 200)
slider_dimensions = (200, 20)
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(slider_position, slider_dimensions),
    start_value=0,
    value_range=(-180, 180),
    manager=ui_manager,
)

clock = pygame.time.Clock()

dragging = False
offset_x = 0
offset_y = 0

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                robot.set_position(robot.get_position()[0] - 2, robot.get_position()[1])
            elif event.key == pygame.K_RIGHT:
                robot.set_position(robot.get_position()[0] + 2, robot.get_position()[1])
            elif event.key == pygame.K_UP:
                robot.set_position(robot.get_position()[0], robot.get_position()[1] - 2)
            elif event.key == pygame.K_DOWN:
                robot.set_position(robot.get_position()[0], robot.get_position()[1] + 2)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if the mouse is over the robot preview
                if robot.cursor_over(event.pos):
                    dragging = True
                    offset_x = event.pos[0] - robot.get_position()[0]
                    offset_y = event.pos[1] - robot.get_position()[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                # Move the robot preview according to the mouse movement
                robot.set_position(event.pos[0] - offset_x, event.pos[1] - offset_y)
        ui_manager.process_events(event)

    win.blit(createImageBG(background_image, win.get_size()), (0, 0))
    win.blit(robot.get_preview(), robot.get_rotated_position())

    ui_manager.update(clock.tick(60) / 1000.0)

    ui_manager.draw_ui(win)

    robot.set_heading(slider.get_current_value())

    print(robot.get_pose())

    pygame.display.update()

pygame.quit()
