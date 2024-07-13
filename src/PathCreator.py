import json
import pygame
import datetime
import math


class PathCreator:
    def __init__(self, win, robot_constants_filename):
        self.win = win
        self.load_constants(robot_constants_filename)
        self.path = "./generated_paths/"

    def load_constants(self, robot_constants_filename):
        with open(robot_constants_filename, "r") as f:
            constants = json.load(f)
            self.width = constants["width"]
            self.length = constants["length"]
            self.wheel_diameter = constants["wheel-diameter"]

    def generate_path(self, robots, filename):
        print("Generating Path...")
        poses = [robot.get_pose() for robot in robots]

        cmds = []

        for i in range(len(poses) - 1):
            pose_from = poses[i]
            pose_to = poses[i + 1]

            a = math.degrees(
                math.atan2(pose_to[1] - pose_from[1], pose_to[0] - pose_from[0])
            )  # degrees
            dist = math.dist(pose_from[:2], pose_to[:2])  # cm

            if pose_from[2] != a:
                cmds.append(f"turn {a}")

            if dist != 0:
                cmds.append(f"move {dist}")

        dateCode = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]

        with open(f"{self.path}{filename}_{dateCode}.txt", "w") as f:
            f.write(f"Generated in {dateCode}\n")
            for cmd in cmds:
                f.write(f"{cmd}\n")

    # --------------------------------- GUI ---------------------------------- #

    def show_lines(self, robots):
        poses_px = [robot.get_center_pose_px() for robot in robots]

        for i in range(len(poses_px) - 1):
            pos1 = poses_px[i][:2]
            pos2 = poses_px[i + 1][:2]

            pygame.draw.line(self.win, (0, 0, 0), pos1, pos2, 2)
