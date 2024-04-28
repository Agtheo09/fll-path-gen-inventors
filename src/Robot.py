import json
from PIL import Image
import pygame


class Robot:
    def __init__(self, constants_filename, preview_image_filename):
        self.constants_filename = constants_filename
        self.load_constants()

        self.preview_image_filename = preview_image_filename
        self.generate_preview()

    def generate_preview(self):
        image = Image.open(self.preview_image_filename)
        resized = image.resize(
            (
                int(150),
                int(150 * image.size[1] / image.size[0]),
            )
        )

        self.preview = pygame.image.fromstring(
            resized.tobytes(), resized.size, resized.mode
        )

    def load_constants(self):
        with open(self.constants_filename, "r") as file:
            constants = json.load(file)
            self.width = constants["width"]
            self.height = constants["height"]
            self.wheel_diameter = constants["wheel-diameter"]

    def get_preview(self):
        return self.preview
