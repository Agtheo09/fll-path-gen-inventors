import pygame
from pygame_gui import UIManager

from src.Robot import Robot
from src.ControlPanel import ControlPanel
from src.Field import Field
from src.Normalizer import Normalizer
from src.Previewer import Previewer

# ----------------------------- Init Window ----------------------------- #
pygame.init()

WIDTH = 1100  # Window Width

# Init Background
field = Field(WIDTH, "./assets/field-masterpiece.png")

field_size = field.getFieldSize()
viewport_size = (field_size[0], field_size[1] + 250)
#

win = pygame.display.set_mode(viewport_size)
pygame.display.set_caption("FLL Path Gen")
pygame.display.set_icon(pygame.image.load("./assets/logo/path-gen-logo-circlural.png"))

background_image = field.getBackground()

# ------------------------ Init Helper Classes ------------------------- #
normalizer = Normalizer(
    WIDTH,
    "./src/constants/field_constants.json",
    "./src/constants/robot_constants.json",
)

previewer = Previewer(
    "./assets/fll_robot.png",
    field_size,
    normalizer.get_size_ratio(),
    normalizer.get_px_per_cm(),
)

robot = Robot(
    initPose=(2, 80, 0),  # cm, cm, degrees
    field_preview_size=field_size,
    preview_size_ratio=normalizer.get_size_ratio(),
    px_per_cm=normalizer.get_px_per_cm(),
    constants_filename="./src/constants/robot_constants.json",
    robot_ortho_preview_size=previewer.get_ortho_preview_size(),
)

ui_manager = UIManager(viewport_size)

controlPanel = ControlPanel(
    ui_manager,
    viewport_size,
    (viewport_size[0], 250),  # width is the same as the field height is 250
    lambda theta: robot.set_heading(theta),
)

# ---------------------------- Util VAriables ---------------------------- #
dragging = False
offset_x = 0
offset_y = 0

clock = pygame.time.Clock()
running = True


while running:
    # ---------------------------- Event Handling ---------------------------- #
    for event in pygame.event.get():
        ui_manager.process_events(event)

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                previewer.add_pose(robot.get_effected_pose())

            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                # Move the robot using arrow keys
                robot.nudge(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left Click
                if robot.is_cursor_over(event.pos):
                    # On Click if cursor is over begin Dragging
                    dragging = True
                    cursorX, cursorY = event.pos
                    offset_x = cursorX - robot.getX_px()
                    offset_y = cursorY - robot.getY_px()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 1 = Left Click
                dragging = False  # Stop dragging
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                # Move Robot
                robot.set_position_px(event.pos[0] - offset_x, event.pos[1] - offset_y)
                pass
        elif event.type == pygame.USEREVENT:
            controlPanel.proccess_events(event)

    # # --------------------------- Reset Window --------------------------- #
    # win.clear()

    # # ----------------------- Draw Background Color ---------------------- #
    win.fill((230, 230, 230))  # gray

    # ---------------------------- Draw Field ---------------------------- #
    win.blit(background_image, (0, 0))

    # ------------------------ Draw Pose History ------------------------- #

    # for pixel_coordinates, pose_preview in previewer.get_poses_history_previews():
    #     win.blit(pose_preview, pixel_coordinates)

    # ---------------------------- Draw Robot ---------------------------- #
    previewer.update_main_preview(robot.get_effected_pose())
    win.blit(previewer.get_main_preview(), robot.get_effected_position())
    # win.blit(previewer.get_main_preview(), (1000, 700))
    # print(field_size)

    # ----------------------------- UI Utils ----------------------------- #
    ui_manager.update(clock.tick(60) / 1000.0)

    ui_manager.draw_ui(win)

    pygame.display.update()

    print(robot.get_effected_pose())

pygame.quit()
