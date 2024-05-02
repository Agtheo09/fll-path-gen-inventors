from PIL import Image
import pygame


class Previewer:
    poses_history = []
    poses_history_previews = []

    def __init__(
        self, robot_image_path, field_preview_size, preview_size_ratio, px_per_cm
    ):
        # Import the Fundamental Image
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

        # SAve the px_per_cm ratio
        self.px_per_cm = px_per_cm

    def cmToPx(self, cm):
        return cm * self.px_per_cm

    def pxToCm(self, px):
        return px / self.px_per_cm

    def pose_to_preview(self, pose):
        return pygame.transform.rotate(self.ortho_image, pose[2])

    def add_pose(self, pose):
        self.poses_history.append(pose)
        self.poses_history_previews.append(
            [(self.cmToPx(pose[0]), self.cmToPx(pose[1])), self.pose_to_preview(pose)]
        )

    def get_poses_history(self):
        return self.poses_history

    def get_poses_history_previews(self):
        return self.poses_history_previews
