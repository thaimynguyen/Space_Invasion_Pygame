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


class TextBox:
    def __init__(self, size, font_color, fill_color=None, x=0, y=0, text="", box=False):
        self.settings = Settings()
        self.size = self.settings.width * size // 100
        self.font_color = font_color
        self.fill_color = fill_color
        self.text = text
        self.x = x
        self.y = y
        self.box = box

    def draw(self, screen):
        if self.text != "":
            font = pygame.font.SysFont("comicsans", self.size)
            if self.box:
                self.text_box = font.render(self.text, True, self.font_color, self.fill_color)
                self.text_rect = self.text_box.get_rect(center=(self.x, self.y))
                screen.blit(self.text_box, self.text_rect)
            else:
                self.text_box = font.render(self.text, True, self.font_color)
                screen.blit(self.text_box, (self.x, self.y))
