from __future__ import annotations
from settings import Settings
import pygame


class Actor:
    def __init__(
        self, width: int, height: int, speed: int, img_path: str, settings: Settings
    ) -> None:
        self.width = width
        self.height = height
        self.speed = speed
        self.image = pygame.transform.scale(
            pygame.image.load(img_path), (self.width, self.height)
        )
        self.settings = settings
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height)
        )
        self.x = None
        self.y = None
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.should_be_removed = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.screen.blit(self.image, (self.x, self.y))

    def check_collision(self, other) -> bool:
        if self == other:
            return False

        x_offset = other.x - self.x
        y_offset = other.y - self.y
        return self.mask.overlap(other.mask, (x_offset, y_offset)) is not None

    def on_collision(self, other):
        pass
