from PIL import Image, ImageOps
import pygame


class Previewer:
    def __init__(
        self, robot_image_path, field_preview_size, preview_size_ratio, px_per_cm
    ):
        # Open the Fundamental Image
        raw_image = Image.open(robot_image_path)

        resized = raw_image.resize(
            (
                int(field_preview_size[0] / preview_size_ratio),
                int(
                    field_preview_size[0]
                    / preview_size_ratio
                    * raw_image.size[1]
                    / raw_image.size[0]
                ),
            )
        )  # Resize the image so the robot-field ratios are good

        self.preview_templete = pygame.image.fromstring(
            resized.tobytes(), resized.size, resized.mode
        )

        resized_greyed = ImageOps.grayscale(resized).convert("RGBA")

        self.grey_preview_templete = pygame.image.fromstring(
            resized_greyed.tobytes(), resized_greyed.size, resized_greyed.mode
        )

        # Save the px_per_cm ratio
        self.px_per_cm = px_per_cm

    # --------------------------------- Util --------------------------------- #
    def get_ortho_preview_size(
        self,
    ):  # Returns the size of the robot preview theta=0deg
        return self.preview_templete.get_size()

    def cmToPx(self, cm):
        return cm * self.px_per_cm

    def pxToCm(self, px):
        return px / self.px_per_cm

    def preview_robot(self, robot):
        if robot.get_isMain():
            return pygame.transform.rotate(self.preview_templete, robot.get_pose()[2])

        return pygame.transform.rotate(self.grey_preview_templete, robot.get_pose()[2])

    # ----------------------------- Main Preview ----------------------------- #

    def update_main_preview(self, robot):
        self.mainPreview = self.preview_robot(robot)

    def get_main_preview(self):
        return self.mainPreview

    def get_main_preview_size(self):
        return self.mainPreview.get_size()
