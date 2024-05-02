from PIL import Image
import pygame


class Previewer:
    mainPreview = None
    poses_history = []
    poses_history_previews = []

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

        self.ortho_image = pygame.image.fromstring(
            resized.tobytes(), resized.size, resized.mode
        )

        # Save the px_per_cm ratio
        self.px_per_cm = px_per_cm

    # -------------------------------------- Util -------------------------------------- #
    def get_ortho_preview_size(self):
        return self.ortho_image.get_size()

    def cmToPx(self, cm):
        return cm * self.px_per_cm

    def pxToCm(self, px):
        return px / self.px_per_cm

    def pose_to_preview(self, pose):
        return pygame.transform.rotate(self.ortho_image, pose[2])

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
                self.pose_to_preview(pose),
            ]
        )

    def get_poses_history(self):
        return self.poses_history

    def get_poses_history_previews(self):
        return self.poses_history_previews
