from typing import List
import pygame
import random
import time

from settings import Settings
from player import PlayerShip, PlayerBullet
from enemy import EnemyShip, EnemyBullet


# RBG
red = (255, 0, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height)
        )
        self.clock = pygame.time.Clock()
        self.actors = []
        self.player_life_count = self.settings.player_max_lives
        self.player_scores = 0
        self.game_over = False
        self.running = True

    def draw_screen(self):
        self.screen.blit(self.settings.background, (0, 0))
        pygame.display.set_caption("Space Invasion Game")
        for actor in self.actors:
            actor.draw()
        self.update_score()
        self.update_health()
        pygame.display.update()

    def update_score(self):
        font = pygame.font.SysFont("comicsans", self.settings.width // 15)
        self.score_text = font.render(f"Score: {str(self.player_scores)}", True, white)
        self.screen.blit(
            self.score_text,
            (self.settings.width // 4 * 3, self.settings.height // 30 * 2),
        )

    def update_health(self):
        font = pygame.font.SysFont("comicsans", self.settings.width // 15)
        self.health_text = font.render(
            f"Health: {str(self.player_life_count)}", True, white
        )
        self.screen.blit(
            self.health_text,
            (self.settings.width // 4 * 3, self.settings.height // 30),
        )

    def update_all(self):
        # Pre-action phase
        for actor in self.actors[:]:
            # update new x, y positions
            actor.update()

            # remove from program when out of screen, counting both top and bottom
            if actor.y > self.settings.height or actor.y < 0:
                self.actors.remove(actor)
                continue

            # enemy ships shoot bullets randomly
            if isinstance(actor, EnemyShip) and not actor.should_be_removed:
                if random.randint(1, self.settings.FPS * 3) == 1:
                    bullet = actor.shoot()
                    self.actors.append(bullet)

            # check collision against all the other objects
            for i in range(len(self.actors)):
                other_actor = self.actors[i]
                if other_actor.check_collision(actor):
                    other_actor.on_collision(actor)

            # remove objects upon collision
            if actor.should_be_removed:
                self.actors.remove(actor)
                if isinstance(actor, PlayerShip):
                    pygame.mixer.Sound("collision_sound.mp3").play()
                    self.reset_player_life()
                    self.player_life_count -= 1
                if isinstance(actor, PlayerBullet):
                    self.player_scores += 1

    def create_enemy(self):
        enemy_ship = EnemyShip(self.settings)
        self.actors.append(enemy_ship)

    def reset_player_life(self):
        if self.player_life_count > 1:
            self.player_ship = PlayerShip(self.settings)
            self.actors.append(self.player_ship)
        else:
            self.game_over = True

    def draw_game_over(self):
        font = pygame.font.SysFont("comicsans", self.settings.width // 5)
        text = font.render("GAME OVER", True, red, white)
        text_rect = text.get_rect()
        text_rect.center = (
            self.settings.width // 2,
            self.settings.height // 2,
        )
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def run(self) -> None:
        self.draw_screen()
        self.reset_player_life()

        while self.running:
            self.clock.tick(self.settings.FPS)

            if pygame.event.get(pygame.QUIT):
                break
            pygame.event.pump()

            self.keys = pygame.key.get_pressed()
            if self.keys[pygame.K_SPACE] and self.player_ship.bullet_cooldown == 0:
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

            if self.game_over:
                self.draw_game_over()
                time.sleep(5)
                break  # Quit program after 5 seconds


if __name__ == "__main__":
    game = Game()
    game.run()
