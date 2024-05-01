import pygame
import pygame_gui
from pygame_gui import UIManager

from PIL import Image

from src.Robot import Robot
from src.ControlPanel import ControlPanel
from src.Field import Field
from src.Normalizer import Normalizer

# Init Window
pygame.init()

WIDTH = 1400

field = Field(WIDTH, "./assets/field-masterpiece.png")

field_size = field.getFieldSize()
viewport_size = (field_size[0], field_size[1] + 250)

background_image = field.getBackground()

win = pygame.display.set_mode(viewport_size)
pygame.display.set_caption("FLL Path Gen")
win.fill((230, 230, 230))

normalizer = Normalizer(
    WIDTH,
    "./src/constants/field_constants.json",
    "./src/constants/robot_constants.json",
)

robot = Robot(
    initPose=(2, 80, 0),
    field_preview_size=field_size,
    preview_size_ratio=normalizer.get_size_ratio(),
    px_per_cm=normalizer.get_px_per_cm(),
    constants_filename="./src/constants/robot_constants.json",
    preview_image_filename="./assets/fll_robot.png",
)

ui_manager = UIManager(viewport_size)

controlPanel = ControlPanel(
    ui_manager,
    viewport_size,
    (viewport_size[0], 250),  # width is the same as the field height is 250
    lambda theta: robot.set_heading(theta),
)

dragging = False
offset_x = 0
offset_y = 0

clock = pygame.time.Clock()
runnning = True


while runnning:
    for event in pygame.event.get():
        ui_manager.process_events(event)

        if event.type == pygame.QUIT:
            runnning = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                robot.nudge(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left Click
                if robot.cursor_over(event.pos):
                    dragging = True
                    cursorX, cursorY = event.pos
                    offset_x = cursorX - robot.getX_px()
                    offset_y = cursorY - robot.getY_px()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left Click
                dragging = False  # Stop dragging
        elif event.type == pygame.MOUSEMOTION:
            # print(offset_x, offset_y)
            if dragging:
                robot.set_position_px(event.pos[0] - offset_x, event.pos[1] - offset_y)
                pass
        elif event.type == pygame.USEREVENT:
            controlPanel.proccess_events(event)

    win.blit(background_image, (0, 0))  # Draw the field
    win.blit(robot.get_preview(), robot.get_effected_position())  # Draw the robot

    ui_manager.update(clock.tick(60) / 1000.0)

    ui_manager.draw_ui(win)

    pygame.display.update()

pygame.quit()
