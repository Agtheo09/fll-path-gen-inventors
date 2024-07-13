import pygame
import pygame_gui


class ControlPanel:
    def __init__(
        self,
        ui_manager,
        viewport_size,
        control_panel_size,
        set_heading,
        add_clone,
        generate_path,
    ):
        self.ui_manager = ui_manager
        self.viewport_size = viewport_size
        self.control_panel_size = control_panel_size

        # Lambdas
        self.set_heading = set_heading
        self.add_clone = add_clone
        self.generate_path = generate_path

        # Offset: This basically moves the UI below the field preview
        self.offset = (
            viewport_size[0] - control_panel_size[0],
            viewport_size[1] - control_panel_size[1],
        )

        # Init Control Panel UI
        self.heading_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                (6 + self.offset[0], 10 + self.offset[1]), (100, 30)
            ),
            initial_text="0",
            placeholder_text="Heading",
            manager=self.ui_manager,
        )
        self.set_heading_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (6 + self.offset[0], 50 + self.offset[1]), (100, 30)
            ),
            text="Set Heading",
            manager=self.ui_manager,
        )
        self.add_pose_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (130 + self.offset[0], 10 + self.offset[1]), (120, 30)
            ),
            text="Add Pose",
            manager=self.ui_manager,
        )

        self.generate_path_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (130 + self.offset[0], 50 + self.offset[1]), (120, 30)
            ),
            text="Generate Path",
            manager=self.ui_manager,
        )

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.set_heading_btn:
                    heading = float(self.heading_input.get_text())
                    self.set_heading(
                        heading,
                        0 if self.robot_selected_idx == -1 else self.robot_selected_idx,
                    )
                if event.ui_element == self.add_pose_btn:
                    self.add_clone()
                if event.ui_element == self.generate_path_btn:
                    self.generate_path()

    def update_selected_robot(self, robot_idx):
        self.robot_selected_idx = robot_idx
