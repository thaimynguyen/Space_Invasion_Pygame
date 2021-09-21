import pygame


class Settings:
    def __init__(self):
        # Set screen size
        self.width = 400
        self.height = 700

        # Load & scale image
        self.background = pygame.transform.scale(
            pygame.image.load("space.jpg"), (self.width, self.height)
        )

        self.FPS = 40  # Set frame per second
        self.invader_frequency = 1500
        self.invader_bullet_limit = 3
        self.spaceship_max_lives = 3
