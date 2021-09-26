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
        self.player_bullet_cooldown = self.FPS // 10
        self.player_max_lives = 3
