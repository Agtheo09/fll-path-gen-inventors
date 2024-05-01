import pygame
from PIL import Image

img = Image.open("assets/fll_robot.png")

# img.show()

resized = img.resize(
    (
        int(700),
        int(700 * img.size[1] / img.size[0]),
    )
)

img2 = pygame.image.fromstring(resized.tobytes(), resized.size, resized.mode)

rotated_image = pygame.transform.rotate(img2, 32)

pygame.init()
win = pygame.display.set_mode(rotated_image.get_size())

running = True
while running:
    win.blit(rotated_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
