from __future__ import annotations
from settings import Settings
import actor
import enemy


class PlayerShip(actor.Actor):
    def __init__(self, settings: Settings) -> None:
        width = 40
        height = 50
        speed = 5
        img_path = "player_ship.png"
        self.settings = settings
        super().__init__(width, height, speed, img_path, settings)

        self.x = (self.settings.width - self.width) // 2
        self.y = self.settings.height - self.height

    def move_left(self) -> None:
        if self.x - self.speed > 0:
            self.x -= self.speed

    def move_right(self) -> None:
        if self.x + self.width + self.speed < self.settings.width:
            self.x += self.speed

    def shoot(self) -> PlayerBullet:
        bullet = PlayerBullet(self.x + 10, self.y - 20, self.settings)
        return bullet

    def on_collision(self, other) -> None:
        if isinstance(other, enemy.EnemyShip) or isinstance(other, enemy.EnemyBullet):
            self.should_be_removed = True


class PlayerBullet(actor.Actor):
    def __init__(self, x: int, y: int, settings: Settings) -> None:
        width = 20
        height = 30
        speed = 10
        img_path = "player_bullet.png"
        self.settings = settings
        super().__init__(width, height, speed, img_path, settings)
        self.x = x
        self.y = y

    def update(self) -> None:
        self.y -= self.speed

    def on_collision(self, other) -> None:
        if isinstance(other, enemy.EnemyShip):
            self.should_be_removed = True
