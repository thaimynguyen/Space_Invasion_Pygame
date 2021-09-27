import sys
import pygame
import random
import time

from settings import Settings, TextBox
from player import PlayerShip, PlayerBullet
from enemy import EnemyShip


# RBG
red = (255, 0, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height)
        )
        self.actors = []
        self.player_life_count = self.settings.player_max_lives
        self.player_scores = 0
        self.game_over = False
        self.running = True
        self.draw_screen()
        self.draw_start_button()

    def draw_screen(self):
        self.screen.blit(self.settings.background, (0, 0))
        pygame.display.set_caption("Space Invasion Game")
        for actor in self.actors:
            actor.draw()
        self.update_score()
        self.update_health()
        pygame.display.update()

    def draw_start_button(self):
        self.start_button = TextBox(20, yellow, text="START", box=True)
        self.start_button.x = self.settings.width // 2
        self.start_button.y = self.settings.height // 2
        self.start_button.draw(self.screen)
        pygame.display.update()

    def update_score(self):
        self.score_board = TextBox(6, white)
        self.score_board.x = self.settings.width - self.score_board.size * 4
        self.score_board.y = self.score_board.size * 2
        self.score_board.text = f"Score: {str(self.player_scores)}"
        self.score_board.draw(self.screen)

    def update_health(self):
        self.health_status = TextBox(6, white)
        self.health_status.x = self.settings.width - self.health_status.size * 4
        self.health_status.y = self.health_status.size
        self.health_status.text = f"Health: {str(self.player_life_count)}"
        self.health_status.draw(self.screen)

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

    def draw_game_over_text(self):
        self.game_over_text = TextBox(20, red, text="GAME OVER", box=True)
        self.game_over_text.x = self.settings.width // 2
        self.game_over_text.y = self.settings.height // 2
        self.game_over_text.draw(self.screen)
        pygame.display.update()

    def draw_new_game_button(self):
        self.new_game_button = TextBox(15, yellow, text="NEW GAME", box=True)
        self.new_game_button.x = self.settings.width // 2
        self.new_game_button.y = int(self.settings.height * 0.6)
        self.new_game_button.draw(self.screen)
        pygame.display.update()

    def run(self) -> None:
        self.reset_player_life()

        while True:
            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()
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
                self.draw_game_over_text()
                self.draw_new_game_button()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.new_game_button.text_rect.collidepoint(event.pos):
                                self.running = False
                                return True
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()


if __name__ == "__main__":
    while True:
        game = Game()
        while game.running:
            clock = pygame.time.Clock()
            clock.tick(game.settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.start_button.text_rect.collidepoint(event.pos):
                        game.run()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
