import json


class Normalizer:
    SIZE_RATIO = 0
    pxPerCm = 0

    def __init__(
        self, field_preview_width, field_constants_filename, robot_constants_filename
    ):
        self.field_preview_width = field_preview_width

        self.field_constants_filename = field_constants_filename
        self.robot_constants_filename = robot_constants_filename

        self.load_data()

        self.calculate_size_ratio()
        self.calculate_px_per_cm()

    def load_data(self):
        with open(self.field_constants_filename) as file:
            field_constants = json.load(file)
            self.FIELD_WIDTH = field_constants["width"]

        with open(self.robot_constants_filename) as file:
            robot_constants = json.load(file)
            self.ROBOT_LENGTH = robot_constants["length"]

    def calculate_size_ratio(self):
        self.SIZE_RATIO = (
            self.FIELD_WIDTH / self.ROBOT_LENGTH
        )  # Field Large Side / Robot Large Side && RATIO > 1

    def calculate_px_per_cm(self):
        self.pxPerCm = self.field_preview_width / self.FIELD_WIDTH

    def get_size_ratio(self):
        return self.SIZE_RATIO

    def get_px_per_cm(self):
        return self.pxPerCm
