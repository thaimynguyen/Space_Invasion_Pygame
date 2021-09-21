from typing import List
import pygame
import random

from settings import Settings
from player import PlayerShip, PlayerBullet
from enemy import EnemyShip, EnemyBullet


# RBG
red = (255, 0, 0)
yellow = (255, 255, 0)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height)
        )
        self.clock = pygame.time.Clock()
        self.actors = []

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

            # check collision
            for other_actor in self.actors:
                if actor.check_collision(other_actor):
                    actor.on_collision(other_actor)

            if actor.should_be_removed:
                self.actors.remove(actor)
                # if isinstance(actor, PlayerShip):
                # self.reset_player_life()

            # enemy ships shoot bullets randomly
            if isinstance(actor, EnemyShip) and not actor.should_be_removed:
                if random.randint(1, self.settings.FPS * 3) == 1:
                    bullet = actor.shoot()
                    self.actors.append(bullet)

    def create_enemy(self):
        enemy_ship = EnemyShip(self.settings)
        self.actors.append(enemy_ship)

    def reset_player_life(self):
        self.player_ship = PlayerShip(self.settings)
        self.actors.append(self.player_ship)

    def run(self) -> None:
        self.draw_screen()
        self.reset_player_life()

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
