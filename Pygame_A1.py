import pygame
import os
from random import randint


class Settings:
    window_width = 600
    window_height = 800
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    fps = 60
    caption = "Ibrahim Aldemir GAME"
    alien_width = 70
    alien_height = 70
    alien_pos_x = 100
    alien_pos_y = 200
    bullet_width = 70
    bullet_height = 70


class Background(pygame.sprite.Sprite):
    def __init__(self, filename="background.png") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))


class Alien(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, "alien.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.alien_width, Settings.alien_height))
        self.rect = self.image.get_rect()
        self.rect.left = Settings.alien_pos_x
        self.rect.top = Settings.alien_pos_y
        self.speed_h = 30
        self.speed_v = 30
        self.lives = 3

    def update(self):
        if self.rect.top >= Settings.window_height - 60:
            self.rect.top = Settings.window_height - 70
        if self.rect.left >= Settings.window_width - 50:
            self.rect.left = Settings.window_width - 50
        if self.rect.top <= 1:
            self.rect.top = 1
        if self.rect.left <= 1:
            self.rect.left = 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, "bullet.png")).convert_alpha()

        scale_ratio = randint(1, 2) / 4
        self.image = pygame.transform.scale(self.image, (
            int(self.image.get_rect().width * scale_ratio),
            int(self.image.get_rect().height * scale_ratio)
        ))

        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = randint(10, 490)
        self.speed_x = randint(1,3)
        self.speed_y = randint(1,3)

    def update(self):
        self.rect.move_ip(0, self.speed_x * self.speed_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Game(object):
    def __init__(self, ) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"


        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.alien = Alien()
        self.bullet = Bullet()

    def run(self):
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw1()
        pygame.quit()

    def update(self):
        self.alien.update()
        self.check_for_collision()
        self.bullet.update()

    def check_for_collision(self):
        self.bullet.hit = pygame.sprite.collide_mask(self.bullet, self.alien)
        if self.bullet.hit:
            self.alien.rect.top = 700
            self.alien.rect.left = 270
            self.alien.lives -= 1

    def draw1(self):
        self.background.draw(self.screen)
        self.alien.draw(self.screen)
        self.bullet.draw(self.screen)
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            # Movment
            if event.type == pygame.KEYDOWN:  # hoch
                if event.key == pygame.K_UP:
                    self.alien.rect.top -= self.alien.speed_h
            if event.type == pygame.KEYDOWN:  # runter
                if event.key == pygame.K_DOWN:
                    self.alien.rect.top += self.alien.speed_h
            if event.type == pygame.KEYDOWN:  # links
                if event.key == pygame.K_LEFT:
                    self.alien.rect.left -= self.alien.speed_v
            if event.type == pygame.KEYDOWN:  # rechts
                if event.key == pygame.K_RIGHT:
                    self.alien.rect.left += self.alien.speed_v


if __name__ == '__main__':
    game = Game()
    game.run()
