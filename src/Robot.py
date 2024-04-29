import json
from PIL import Image
import pygame


class Robot:
    def __init__(
        self, initPose, field_preview_size, constants_filename, preview_image_filename
    ):
        self.x, self.y, self.heading = initPose
        self.effected_position = (0, 0)  # Preview Position (changes due to rotation)

        self.constants_filename = constants_filename
        self.load_constants()

        self.preview_image_filename = preview_image_filename
        self.generate_preview()

        self.field_preview_size = field_preview_size

    def generate_preview(self):
        image = Image.open(self.preview_image_filename)
        resized = image.resize(
            (
                int(150),
                int(150 * image.size[1] / image.size[0]),
            )
        )

        ortho_image = pygame.image.fromstring(
            resized.tobytes(), resized.size, resized.mode
        )
        rotated_image = pygame.transform.rotate(ortho_image, self.heading)

        original_size = ortho_image.get_size()
        self.rotated_size = rotated_image.get_size()

        self.rotated_position = (
            self.x + (original_size[0] - self.rotated_size[0]) // 2,
            self.y + (original_size[1] - self.rotated_size[1]) // 2,
        )

        self.preview = rotated_image.copy()

    def load_constants(self):
        with open(self.constants_filename, "r") as file:
            constants = json.load(file)
            self.width = constants["width"]
            self.height = constants["height"]
            self.wheel_diameter = constants["wheel-diameter"]

    def get_preview(self):
        return self.preview

    def set_position(self, x, y):
        self.x = (
            x
            if x >= 0 and x < self.field_preview_size[0] - self.rotated_size[0]
            else self.x
        )
        self.y = (
            y
            if y >= 0 and y < self.field_preview_size[1] - self.rotated_size[1]
            else self.y
        )

    def set_heading(self, heading):
        self.heading = heading
        self.generate_preview()

    def get_position(self):
        return (self.x, self.y)

    def get_rotated_position(self):
        return self.rotated_position

    def get_heading(self):
        return self.heading

    def get_pose(self):
        return (self.x, self.y, self.heading)

    def cursor_over(self, cursor_position):
        x, y = cursor_position
        rx, ry = self.rotated_position
        width, height = self.preview.get_size()

        return rx <= x <= rx + width and ry <= y <= ry + height
