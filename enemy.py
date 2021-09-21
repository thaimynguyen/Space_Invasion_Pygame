from __future__ import annotations
from settings import Settings
import actor
import player
import random


class EnemyShip(actor.Actor):
    def __init__(self, settings: Settings) -> None:
        width = 20
        height = 25
        speed = 2
        img_path = "enemy_ship.png"
        self.settings = settings
        super().__init__(width, height, speed, img_path, settings)

        self.x = random.randint(0, self.settings.width - self.width)
        self.y = 0

    def update(self) -> None:
        self.y += self.speed

    def shoot(self) -> EnemyBullet:
        bullet = EnemyBullet(self.x, self.y + 10, self.settings)
        return bullet

    def on_collision(self, other) -> None:
        if isinstance(other, player.PlayerShip) or isinstance(other, player.PlayerBullet):
            self.should_be_removed = True


class EnemyBullet(actor.Actor):
    def __init__(self, x: int, y: int, settings: Settings) -> None:
        width = 20
        height = 15
        speed = 10
        img_path = "enemy_bullet.png"
        self.settings = settings
        super().__init__(width, height, speed, img_path, settings)
        self.x = x
        self.y = y

    def update(self) -> None:
        self.y += self.speed

    def on_collision(self, other) -> None:
        if isinstance(other, player.PlayerShip):
            self.should_be_removed = True
