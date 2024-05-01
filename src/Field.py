from PIL import Image
import pygame


class Field:
    def __init__(self, width, image_path):
        self.image_raw = Image.open(image_path)

        self.field_size = (
            int(width),
            int(
                width * self.image_raw.size[1] / self.image_raw.size[0]
            ),  # Ratio should be around 0.566
        )

        self.bgWig = self.convertToWig(self.image_raw, self.field_size)

    def getFieldSize(self):
        return self.field_size

    def convertToWig(self, image, size):
        resized = image.resize(size)

        return pygame.image.fromstring(resized.tobytes(), resized.size, resized.mode)

    def getBackground(self):
        return self.bgWig
