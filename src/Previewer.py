from PIL import Image, ImageOps
import pygame


class Previewer:
    def __init__(
        self, robot_image_path, field_preview_size, preview_size_ratio, px_per_cm
    ):
        self.field_preview_size = field_preview_size
        self.preview_size_ratio = preview_size_ratio

        # Open the Fundamental Image
        raw_image = Image.open(f"{robot_image_path}/robot.png").convert("RGBA")
        blue_image = Image.open(f"{robot_image_path}/robot_blue.png").convert("RGBA")
        grey_image = Image.open(f"{robot_image_path}/robot_grey.png").convert("RGBA")

        rgb_resized = self.resize_image(raw_image)
        main_preview_template = pygame.image.fromstring(
            rgb_resized.tobytes(), rgb_resized.size, rgb_resized.mode
        )

        grey_resized = self.resize_image(grey_image)
        clone_preview_template = pygame.image.fromstring(
            grey_resized.tobytes(), grey_resized.size, grey_resized.mode
        )

        blue_resized = self.resize_image(blue_image)
        selected_preview_template = pygame.image.fromstring(
            blue_resized.tobytes(), blue_resized.size, blue_resized.mode
        )

        self.templates = [
            main_preview_template,
            clone_preview_template,
            selected_preview_template,
        ]

        # Save the px_per_cm ratio
        self.px_per_cm = px_per_cm

    # -------------------------- Image Manipulation -------------------------- #
    def resize_image(self, image):
        return image.resize(
            (
                int(self.field_preview_size[0] / self.preview_size_ratio),
                int(
                    self.field_preview_size[0]
                    / self.preview_size_ratio
                    * image.size[1]
                    / image.size[0]
                ),
            )
        )  # Resize the image so the robot-field ratios are good

    # --------------------------------- Util --------------------------------- #
    def get_ortho_preview_size(
        self,
    ):  # Returns the size of the robot preview theta=0deg
        return self.templates[0].get_size()

    def cmToPx(self, cm):
        return cm * self.px_per_cm

    def pxToCm(self, px):
        return px / self.px_per_cm

    # --------------------------- Preview Functions -------------------------- #

    def preview_robot(self, robot):
        if robot.is_selected():
            return pygame.transform.rotate(self.templates[2], robot.get_pose()[2])
        elif robot.get_isMain():
            return pygame.transform.rotate(self.templates[0], robot.get_pose()[2])

        return pygame.transform.rotate(self.templates[1], robot.get_pose()[2])
