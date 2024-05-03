from PIL import Image, ImageOps
import pygame
import numpy as np


class Previewer:
    mainPreview = None
    poses_history = []
    poses_history_previews = []

    greying_alpha = 0.4

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
        )

        resized_greyed = ImageOps.grayscale(resized).convert("RGBA")

        self.main_preview_templete = pygame.image.fromstring(
            resized.tobytes(), resized.size, resized.mode
        )

        self.history_preview_templete = pygame.image.fromstring(
            resized_greyed.tobytes(), resized_greyed.size, resized_greyed.mode
        )

        # Save the px_per_cm ratio
        self.px_per_cm = px_per_cm

    # -------------------------------------- Util -------------------------------------- #
    def get_ortho_preview_size(self):
        return self.main_preview_templete.get_size()

    def cmToPx(self, cm):
        return cm * self.px_per_cm

    def pxToCm(self, px):
        return px / self.px_per_cm

    def pose_to_preview(self, pose, isMain=True):
        if isMain:
            return pygame.transform.rotate(self.main_preview_templete, pose[2])
        else:
            return pygame.transform.rotate(self.history_preview_templete, pose[2])

    # ---------------------------------- Main Preview ---------------------------------- #

    def update_main_preview(self, pose):
        self.mainPreview = self.pose_to_preview(pose)

    def get_main_preview(self):
        return self.mainPreview

    def get_main_preview_size(self):
        return self.mainPreview.get_size()

    # ---------------------------------- Poses History --------------------------------- #
    def add_pose(self, pose):
        self.poses_history.append(pose)
        self.poses_history_previews.append(
            [
                (pose[0], pose[1]),
                self.pose_to_preview(pose, False),
            ]
        )

    def get_poses_history(self):
        return self.poses_history

    def get_poses_history_previews(self):
        return self.poses_history_previews
