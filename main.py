import pygame
from pygame_gui import UIManager

from src.Robot import Robot
from src.ControlPanel import ControlPanel
from src.Field import Field
from src.Normalizer import Normalizer
from src.Previewer import Previewer

# ------------------------------- Init Window -------------------------------- #
pygame.init()

WIDTH = 1100  # Window Width (Configurable)

# Init Background
field = Field(WIDTH, "./assets/field-masterpiece.png")

field_size = field.getFieldSize()
viewport_size = (
    field_size[0],
    field_size[1] + 250,
)  # 250 = height of the control panel
#

win = pygame.display.set_mode(viewport_size)
pygame.display.set_caption("FLL Path Gen")
pygame.display.set_icon(pygame.image.load("./assets/logo/path-gen-logo-circle.png"))

background_image = field.getBackground()
bg_color = (200, 200, 200)  # gray
# --------------------------- Init Helper Classes ---------------------------- #
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

main_robot = Robot(
    init_pose=(2, 80, 0),  # cm, cm, degrees
    field_preview_size=field_size,
    preview_size_ratio=normalizer.get_size_ratio(),
    px_per_cm=normalizer.get_px_per_cm(),
    constants_filename="./src/constants/robot_constants.json",
    robot_ortho_preview_size=previewer.get_ortho_preview_size(),
)
robots = [main_robot]

ui_manager = UIManager(viewport_size)

controlPanel = ControlPanel(
    ui_manager,
    viewport_size,
    (viewport_size[0], 250),  # width is the same as the field height is 250
    lambda theta: robots[0].set_heading(theta),
    lambda: robots.append(robots[0].generate_clone()),
)

# ------------------------------ Util VAriables ------------------------------ #
dragging_idx = -1  # -1 means no dragging, 0 main robot, 1+ clones
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
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                # Move the robot using arrow keys
                robots[0].nudge_position(
                    event.key
                )  # TODO This should change to active robot instead of main robot
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left Click
                for i, robot in enumerate(robots):
                    if robot.is_cursor_over_smart(event.pos):
                        # On Click if cursor is over begin Dragging
                        dragging_idx = i

                        # Priority to Main Robot
                        if robots[0].is_cursor_over_smart(event.pos):
                            dragging_idx = 0

                        cursorX, cursorY = event.pos
                        robotXpx, robotYpx, _ = robot.get_pose_px()
                        offset_x = cursorX - robotXpx
                        offset_y = cursorY - robotYpx
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 1 = Left Click
                dragging_idx = -1
        elif event.type == pygame.MOUSEMOTION:
            if dragging_idx > -1:
                # Move Robot
                robots[dragging_idx].set_position_px(
                    event.pos[0] - offset_x, event.pos[1] - offset_y
                )
                pass
        elif event.type == pygame.USEREVENT:
            controlPanel.process_events(event)

    # # ---------------------------- Reset Window ---------------------------- #
    # win.clear() # TODO Check this if it is malakia

    # # ------------------------ Draw Background Color ----------------------- #
    win.fill(bg_color)

    # ------------------------------ Draw Field ------------------------------ #
    win.blit(background_image, (0, 0))

    # ----------------------------- Draw Clones ------------------------------ #
    for clone in robots[1:]:
        win.blit(
            previewer.preview_robot(clone),
            clone.get_effected_position(),
        )

    # --------------------------- Draw Main Robot ---------------------------- #
    #  Main robot Goes After clones So it is Always on TOP in window LAYERING

    previewer.update_main_preview(robots[0])
    win.blit(previewer.get_main_preview(), robots[0].get_effected_position())

    # ------------------------------- UI Utils ------------------------------- #
    ui_manager.update(clock.tick(60) / 1000.0)

    ui_manager.draw_ui(win)

    # for pt in robots[0].get_preview_points():
    #     pygame.draw.circle(win, (255, 255, 0), pt, 5)

    pygame.display.update()

pygame.quit()
