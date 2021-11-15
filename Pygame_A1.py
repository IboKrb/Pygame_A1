import pygame
import os


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


class Background(object):
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
        self.speed_h = 10
        self.speed_v = 10

    def move(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.rect.top -= self.speed_h
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.rect.top += self.speed_h
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect.left -= self.speed_v
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.rect.left += self.speed_v

        if self.rect.top == Settings.window_height :
            self.rect.top = 0
        if self.rect.left == Settings.window_width:
            self.rect.left = 0
        if self.rect.top <= -1:
            self.rect.top = Settings.window_height
        if self.rect.left <= -1:
            self.rect.left = Settings.window_width


    def draw(self, screen):
        screen.blit(self.image, self.rect)

class bullet(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, "bullet.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(Settings.bullet_width, Settings.bullet_height))
        self.rect = self.image.get_rect()
        self.rect.left = Settings.alien_pos_x
        self.rect.top = Settings.alien_pos_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

if __name__ == "__main__":
    os.environ['SDL_VIDEO_WINDOW_POS'] = "200,100"

    pygame.init()
    pygame.display.set_caption(Settings.caption)
    screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
    clock = pygame.time.Clock()
    background = Background()

    alien = Alien()

    running = True
    while running:
        clock.tick(Settings.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        background.draw(screen)
        alien.draw(screen)
        alien.update()
        pygame.display.flip()
    pygame.quit()
