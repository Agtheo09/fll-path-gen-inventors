import json
import math
import pygame


class Robot:
    nudge_step = 2

    def __init__(
        self,
        initPose,
        field_preview_size,
        preview_size_ratio,
        px_per_cm,
        constants_filename,
        robot_ortho_preview_size,
    ):
        self.field_preview_size = field_preview_size
        self.robot_ortho_preview_size = robot_ortho_preview_size
        self.robot_preview_size = (0, 0)

        self.preview_size_ratio = preview_size_ratio

        self.px_per_cm = px_per_cm

        self.constants_filename = constants_filename
        self.load_constants()

        self.x, self.y, self.heading = initPose  # Position (cm), Heading (degrees)
        self.x_px = int(self.cmToPx(self.x))
        self.y_px = int(self.cmToPx(self.y))

        self.calculate_preview_size()

        self.effected_position = self.calculate_effected_position(
            self.x_px, self.y_px
        )  # Preview Position (changes due to rotation)

    # -------------------------------------- Util -------------------------------------- #
    def load_constants(self):
        with open(self.constants_filename, "r") as file:
            constants = json.load(file)
            self.width = constants["width"]
            self.length = constants["length"]
            self.wheel_diameter = constants["wheel-diameter"]

    def cmToPx(self, cm):
        return cm * self.px_per_cm

    def pxToCm(self, px):
        return px / self.px_per_cm

    def calculate_preview_size(self):
        self.robot_preview_size = (
            int(
                math.fabs(
                    math.sin(math.radians(self.heading))
                    * self.robot_ortho_preview_size[1]
                )
                + math.fabs(math.cos(math.radians(self.heading)))
                * self.robot_ortho_preview_size[0]
            ),
            int(
                math.fabs(
                    math.sin(math.radians(self.heading))
                    * self.robot_ortho_preview_size[0]
                )
                + math.fabs(math.cos(math.radians(self.heading)))
                * self.robot_ortho_preview_size[1]
            ),
        )

    def calculate_effected_position(self, x, y):
        return (
            x
            + int((self.robot_ortho_preview_size[0] - self.robot_preview_size[0]) // 2),
            y
            + int((self.robot_ortho_preview_size[1] - self.robot_preview_size[1]) // 2),
        )

    def nudge(self, key):
        if key == pygame.K_LEFT:
            self.set_position_px(self.x_px - self.nudge_step, self.y_px)
        elif key == pygame.K_RIGHT:
            self.set_position_px(self.x_px + self.nudge_step, self.y_px)
        elif key == pygame.K_UP:
            self.set_position_px(self.x_px, self.y_px - self.nudge_step)
        elif key == pygame.K_DOWN:
            self.set_position_px(self.x_px, self.y_px + self.nudge_step)

    # ------------------------------------ Setters ------------------------------------ #

    def set_position(self, x, y):
        self.x = (
            self.cmToPx(x)
            if self.cmToPx(x) >= 0
            and self.cmToPx(x) < self.field_preview_size[0] - self.robot_preview_size[0]
            else self.x
        )
        self.y = (
            self.cmToPx(y)
            if self.cmToPx(y) >= 0
            and self.cmToPx(y) < self.field_preview_size[1] - self.robot_preview_size[1]
            else self.y
        )

        self.x_px = int(self.cmToPx(self.x))
        self.y_px = int(self.cmToPx(self.y))

        self.effected_position = self.calculate_effected_position(self.x_px, self.y_px)

    def set_position_px(self, newXPx, newYPx):
        newCoordinates = self.calculate_effected_position(newXPx, newYPx)

        self.x_px = (
            int(newXPx)
            if newCoordinates[0] >= 0
            and newCoordinates[0]
            < self.field_preview_size[0] - self.robot_preview_size[0]
            else self.x_px
        )
        self.y_px = (
            int(newYPx)
            if newCoordinates[1] >= 0
            and newCoordinates[1]
            < self.field_preview_size[1] - self.robot_preview_size[1]
            else self.y_px
        )

        self.x = int(self.pxToCm(self.x_px))
        self.y = int(self.pxToCm(self.y_px))

        self.effected_position = self.calculate_effected_position(self.x_px, self.y_px)

    def set_heading(self, heading):
        self.heading = heading

        self.calculate_preview_size()

        self.effected_position = self.calculate_effected_position(
            self.x_px, self.y_px
        )  # Position Changed due to rotation

    # ------------------------------------ Getters ------------------------------------ #

    def get_position(self):
        return (self.x, self.y)

    def get_effected_position(self):
        return self.effected_position

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getX_px(self):
        return self.x_px

    def getY_px(self):
        return self.y_px

    def get_heading(self):
        return self.heading

    def get_pose(self):
        return (self.x, self.y, self.heading)

    def get_pose_px(self):
        return (self.x_px, self.y_px, self.heading)

    def get_effected_pose(self):
        return (*self.effected_position, self.heading)

    def is_cursor_over(
        self, cursor_position
    ):  # TODO Too Simple. THis calculated bounding box. Need to calculate the rotated box
        cursor_x, cursor_y = cursor_position
        rx, ry = self.effected_position
        preview_width, preview_height = self.robot_preview_size

        return (
            rx <= cursor_x <= rx + preview_width
            and ry <= cursor_y <= ry + preview_height
        )
