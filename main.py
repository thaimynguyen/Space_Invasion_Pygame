from __future__ import annotations
from typing import List
import pygame
import random


# RBG
red = (255, 0, 0)
yellow = (255, 255, 0)


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

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.screen.blit(self.image, (self.x, self.y))

    def check_collision(self, other) -> bool:
        x_offset = other.x - self.x
        y_offset = other.y - self.y
        return self.mask.overlap(other.mask, (x_offset, y_offset)) is not None


class PlayerShip(Actor):
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

    def update(self) -> None:
        pass

    def shoot(self) -> PlayerBullet:
        bullet = PlayerBullet(self.x + 10, self.y - 20, self.settings)
        return bullet


class EnemyShip(Actor):
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


class PlayerBullet(Actor):
    def __init__(self, x: int, y: int, settings: Settings) -> None:
        width = 20
        height = 30
        speed = 5
        img_path = "player_bullet.png"
        self.settings = settings
        super().__init__(width, height, speed, img_path, settings)
        self.x = x
        self.y = y

    def update(self) -> None:
        self.y -= self.speed


class EnemyBullet(Actor):
    def __init__(self, x: int, y: int, settings: Settings) -> None:
        width = 20
        height = 30
        speed = 3
        img_path = "enemy_bullet.png"
        self.settings = settings
        super().__init__(width, height, speed, img_path, settings)
        self.x = x
        self.y = y
        self.life_used = 0

    def update(self) -> None:
        self.y += self.speed


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height)
        )
        self.clock = pygame.time.Clock()
        self.actors = []
        self.player_bullets = []
        self.player_ship = PlayerShip(self.settings)
        self.actors.append(self.player_ship)

    # def create_new_life(self) -> PlayerShip:
    # player_ship = PlayerShip(self.settings)
    # self.actors.append(player_ship)

    def draw_screen(self):
        self.screen.blit(self.settings.background, (0, 0))
        pygame.display.set_caption("Space Invasion Game")
        for actor in self.actors:
            actor.draw()
        pygame.display.update()

    def update_all(self):
        for actor in self.actors:
            # update new x, y positions
            actor.update()

            # remove from program when out of screen
            if actor.y > self.settings.height:
                self.actors.remove(actor)

            # remove upon collision
            # if isinstance(actor, EnemyShip) or isinstance(actor, EnemyBullet):
            #     if self.player_ship and self.player_ship.check_collision(actor):
            #         self.actors.remove(actor)

            #         try:
            #             self.actors.remove(self.player_ship)
            #             self.life_used += 1
            #         except ValueError:
            #             pygame.quit()
                        # self.reset_player_life()

            # enemy ships shoot bullets randomly
            if isinstance(actor, EnemyShip):
                if random.randint(1, self.settings.FPS * 3) == 1:
                    bullet = actor.shoot()
                    self.player_bullets.append(bullet)
                    self.actors.append(bullet)

    def create_enemy(self):
        enemy = EnemyShip(self.settings)
        self.actors.append(enemy)

    def reset_player_life(self):
        pass

    def run(self) -> None:
        self.draw_screen()
        # self.create_new_life()

        while True:
            self.clock.tick(self.settings.FPS)

            if pygame.event.get(pygame.QUIT):
                break
            pygame.event.pump()

            self.keys = pygame.key.get_pressed()
            if self.keys[pygame.K_SPACE]:
                pygame.mixer.Sound("bullet_sound.mp3").play()
                bullet = self.player_ship.shoot()
                self.actors.append(bullet)

            if self.keys[pygame.K_LEFT]:
                self.player_ship.move_left()

            if self.keys[pygame.K_RIGHT]:
                self.player_ship.move_right()

            if random.randint(1, self.settings.FPS * 2) == 1:
                self.create_enemy()

            self.update_all()
            self.draw_screen()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
