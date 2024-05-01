import json
from PIL import Image
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
        preview_image_filename,
    ):
        self.field_preview_size = field_preview_size

        self.preview_size_ratio = preview_size_ratio

        self.px_per_cm = px_per_cm

        self.constants_filename = constants_filename
        self.load_constants()

        self.x, self.y, self.heading = initPose  # Position (cm), Heading (degrees)
        self.x_px = self.cmToPx(self.x)
        self.y_px = self.cmToPx(self.y)
        self.effected_position = (0, 0)  # Preview Position (changes due to rotation)

        self.preview_image_filename = preview_image_filename
        self.generate_preview()
        self.rotate_preview()

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

    def generate_preview(self):
        image = Image.open(self.preview_image_filename)
        resized = image.resize(
            (
                int(self.field_preview_size[0] / self.preview_size_ratio),
                int(
                    self.field_preview_size[0]
                    / self.preview_size_ratio
                    * image.size[1]
                    / image.size[0]
                ),
            )
        )  # TODO

        self.ortho_image = pygame.image.fromstring(
            resized.tobytes(), resized.size, resized.mode
        )

    def rotate_preview(self):
        rotated_image = pygame.transform.rotate(self.ortho_image, self.heading)

        original_size = self.ortho_image.get_size()
        self.rotated_size = rotated_image.get_size()

        self.effected_position = (
            self.x_px + (original_size[0] - self.rotated_size[0]) // 2,
            self.y_px + (original_size[1] - self.rotated_size[1]) // 2,
        )

        self.preview = rotated_image.copy()

    def get_preview(self):
        return self.preview

    def set_position(self, x, y):
        self.x = (
            self.cmToPx(x)
            if self.cmToPx(x) >= 0
            and self.cmToPx(x) < self.field_preview_size[0] - self.rotated_size[0]
            else self.x
        )
        self.y = (
            self.cmToPx(y)
            if self.cmToPx(y) >= 0
            and self.cmToPx(y) < self.field_preview_size[1] - self.rotated_size[1]
            else self.y
        )

        self.x_px = self.cmToPx(self.x)
        self.y_px = self.cmToPx(self.y)

    def set_position_px(self, newXPx, newYPx):
        self.x_px = (
            newXPx
            if newXPx >= 0
            and newXPx < self.field_preview_size[0] - self.rotated_size[0]
            else self.x_px
        )
        self.y_px = (
            newYPx
            if newYPx >= 0
            and newYPx < self.field_preview_size[1] - self.rotated_size[1]
            else self.y_px
        )

        self.x = self.pxToCm(self.x_px)
        self.y = self.pxToCm(self.y_px)

    def nudge(self, key):
        if key == pygame.K_LEFT:
            self.set_position_px(self.x_px - self.nudge_step, self.y_px)
        elif key == pygame.K_RIGHT:
            self.set_position_px(self.x_px + self.nudge_step, self.y_px)
        elif key == pygame.K_UP:
            self.set_position_px(self.x_px, self.y_px - self.nudge_step)
        elif key == pygame.K_DOWN:
            self.set_position_px(self.x_px, self.y_px + self.nudge_step)

    def set_heading(self, heading):
        self.heading = heading
        self.rotate_preview()

    def get_position(self):
        return (self.x, self.y)

    def get_effected_position(self):
        self.rotate_preview()  # Recalculate the effected position
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

    def cursor_over(self, cursor_position):
        cursor_x, cursor_y = cursor_position
        rx, ry = self.effected_position
        preview_width, preview_height = self.preview.get_size()

        return (
            rx <= cursor_x <= rx + preview_width
            and ry <= cursor_y <= ry + preview_height
        )
