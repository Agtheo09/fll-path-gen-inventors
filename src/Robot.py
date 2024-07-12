import json
import math
import pygame
import numpy as np
import cv2 as cv
from enum import Enum


class Robot:
    isMain = False
    nudge_step = 2  # px
    selected = False

    def __init__(
        self,
        init_pose,
        field_preview_size,
        preview_size_ratio,
        px_per_cm,
        constants_filename,
        robot_ortho_preview_size,
        isMainRobot=True,
    ):
        self.field_preview_size = field_preview_size
        self.robot_ortho_preview_size = robot_ortho_preview_size
        self.robot_preview_size = (0, 0)

        self.preview_size_ratio = preview_size_ratio

        self.px_per_cm = px_per_cm

        self.constants_filename = constants_filename
        self.load_constants()

        self.x, self.y, self.heading = init_pose
        self.x_px = self.cmToPx(self.x)
        self.y_px = self.cmToPx(self.y)

        self.calculate_preview_size()

        self.effected_position = self.calculate_effected_position(self.x_px, self.y_px)

        self.isMain = isMainRobot

        self.is_cursor_over_smart((0, 0))  # TODO remove this malakia

    # -------------------------------------- Util -------------------------------------- #
    def load_constants(self):
        with open(self.constants_filename, "r") as file:
            constants = json.load(file)
            self.width = constants["width"]
            self.length = constants["length"]
            self.wheel_diameter = constants["wheel-diameter"]

    def cmToPx(self, cm):
        return int(cm * self.px_per_cm)

    def pxToCm(self, px):
        return px / self.px_per_cm

    # The size of the picture changes on rotation
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

    # effected_position = is the center of the robot when rotated
    def calculate_effected_position(self, x, y):
        return (
            x
            + int((self.robot_ortho_preview_size[0] - self.robot_preview_size[0]) // 2),
            y
            + int((self.robot_ortho_preview_size[1] - self.robot_preview_size[1]) // 2),
        )

    def nudge_position(self, key):
        if key == pygame.K_LEFT:
            self.set_position_px(self.x_px - self.nudge_step, self.y_px)
        elif key == pygame.K_RIGHT:
            self.set_position_px(self.x_px + self.nudge_step, self.y_px)
        elif key == pygame.K_UP:
            self.set_position_px(self.x_px, self.y_px - self.nudge_step)
        elif key == pygame.K_DOWN:
            self.set_position_px(self.x_px, self.y_px + self.nudge_step)

    # -------------------------------- Setters ------------------------------- #

    def set_position(self, x, y):
        self.x = (
            x
            if self.cmToPx(x) >= 0
            and self.cmToPx(x) < self.field_preview_size[0] - self.robot_preview_size[0]
            else self.x
        )
        self.y = (
            y
            if self.cmToPx(y) >= 0
            and self.cmToPx(y) < self.field_preview_size[1] - self.robot_preview_size[1]
            else self.y
        )

        self.x_px = self.cmToPx(self.x)  # Update Position in px
        self.y_px = self.cmToPx(self.y)  # Update Position in px

        self.effected_position = self.calculate_effected_position(
            self.x_px, self.y_px
        )  # Position Changed due to rotation

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

        self.x = self.pxToCm(self.x_px)  # Update Position in cm
        self.y = self.pxToCm(self.y_px)  # Update Position in cm

        self.effected_position = self.calculate_effected_position(
            self.x_px, self.y_px
        )  # Position Changed due to rotation

    def set_heading(self, heading):
        self.heading = heading  # deg

        # This should run b4 calculating effected position
        self.calculate_preview_size()

        self.effected_position = self.calculate_effected_position(
            self.x_px, self.y_px
        )  # Position Changed due to rotation

    def calculate_corners(self):
        rx, ry = self.effected_position
        preview_width, preview_height = self.robot_preview_size

        a = math.cos(math.radians(self.heading)) * self.cmToPx(self.length)
        b = math.sin(math.radians(self.heading)) * self.cmToPx(self.width)
        c = math.sin(math.radians(self.heading)) * self.cmToPx(self.length)
        d = math.cos(math.radians(self.heading)) * self.cmToPx(self.width)

        self.ptA = (a + rx, 0 + ry)
        self.ptB = (preview_width + rx, d + ry)
        self.ptC = (b + rx, preview_height + ry)
        self.ptD = (0 + rx, c + ry)

    # -------------------------------- Getters ------------------------------- #
    def get_position(self):
        return (self.x, self.y)

    def get_effected_position(self):
        return self.effected_position

    def get_heading(self):
        return self.heading

    def get_pose(self):
        return (self.x, self.y, self.heading)

    def get_pose_px(self):
        return (self.x_px, self.y_px, self.heading)

    def get_effected_pose(self):
        return (*self.effected_position, self.heading)

    # ----------------------------- GUI Related ------------------------------ #
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

    def is_cursor_over_smart(self, cursor_position):
        cursor_x, cursor_y = cursor_position

        return (
            cv.pointPolygonTest(
                np.array(self.get_preview_points(), dtype=np.int32),
                (cursor_x, cursor_y),
                False,
            )
            >= 0
        )

    def get_preview_points(self):
        self.calculate_corners()
        return [self.ptA, self.ptB, self.ptC, self.ptD]

    # ----------------- Cloning (Add Pose to the Trajectory) ----------------- #
    def generate_clone(self):
        return Robot(
            self.get_pose(),
            self.field_preview_size,
            self.preview_size_ratio,
            self.px_per_cm,
            self.constants_filename,
            self.robot_ortho_preview_size,
            False,
        )

    def get_isMain(self):
        return self.isMain

    def select_robot(self):  # Selects the robot for nudging
        self.selected = True

    def deselect_robot(self):
        self.selected = False

    def is_selected(self):
        return self.selected
