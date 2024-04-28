import pygame
import pygame_gui

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Pygame GUI Slider Example")

# Create a UI manager
ui_manager = pygame_gui.UIManager((400, 300))

# Create a horizontal slider
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 100), (300, 30)),
    start_value=0.5,
    value_range=(0.0, 1.0),
    manager=ui_manager,
)

# Create a label to display the slider value
slider_value_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((180, 50), (100, 30)),
    text="Slider Value: 0.50",
    manager=ui_manager,
)

# Run the main loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Pass events to the UI manager
        ui_manager.process_events(event)

    # Update the UI manager
    ui_manager.update(time_delta)

    # Draw the UI manager
    screen.fill((255, 255, 255))
    ui_manager.draw_ui(screen)

    # Update the label with the slider value
    slider_value_label.set_text(f"Slider Value: {slider.get_current_value():.2f}")

    pygame.display.flip()

# Quit Pygame
pygame.quit()
