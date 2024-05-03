import pygame
import pygame_gui


class ControlPanel:
    def __init__(
        self, ui_manager, viewport_size, control_panel_size, set_heading, add_pose
    ):
        self.ui_manager = ui_manager
        self.viewport_size = viewport_size
        self.control_panel_size = control_panel_size

        # Lambdas
        self.set_heading = set_heading
        self.add_pose = add_pose

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
                (130 + self.offset[0], 10 + self.offset[1]), (100, 30)
            ),
            text="Add Pose",
            manager=self.ui_manager,
        )

    def proccess_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.set_heading_btn:
                    heading = float(self.heading_input.get_text())
                    self.set_heading(heading)
                if event.ui_element == self.add_pose_btn:
                    self.add_pose()
