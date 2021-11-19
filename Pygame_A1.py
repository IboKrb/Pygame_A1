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
    alien_pos_x = 250
    alien_pos_y = 600
    bullet_width = 70
    bullet_height = 70
    nof_bullets = 6
    punkte = 0
    heart_width = 80
    heart_height = 60
    lives = 3

class Frontground(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, "heart.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.heart_width, Settings.heart_height))


    def draw(self, screen):
        screen.blit(self.image, (0, 0))

        punkte = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        punktetxt=punkte.render(f"Punkte:{Settings.punkte}",1,(255,255,255))
        screen.blit(punktetxt,(420,750))

        lives = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        livestxt=lives.render(f"x{Settings.lives}",1,(255,255,255))
        screen.blit(livestxt,(60,20))

class Background(pygame.sprite.Sprite):
    def __init__(self, filename="background.png") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
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
        self.speed_h = 40
        self.speed_v = 40
        self.lives = Settings.lives

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

        scale_ratio = randint(1, 3) / 4
        self.image = pygame.transform.scale(self.image, (
            int(self.image.get_rect().width * scale_ratio),
            int(self.image.get_rect().height * scale_ratio)
        ))

        self.image = self.image
        self.rect = self.image.get_rect()
        self.speed_x = randint(1,3)
        self.speed_y = randint(1,3)

    def update(self):
        self.rect.move_ip(0, self.speed_x * self.speed_y)
        if self.rect.top >= Settings.window_height:
            self.rect.centerx = randint(0,Settings.window_width)
            self.rect.centery = randint(0,10)
            Settings.punkte += 4

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
        self.frontground= Frontground()
        self.background = Background()
        self.bullet = Bullet()
        self.alien = Alien()
        self.all_bullets = pygame.sprite.Group()
        self.all_bullets.add(self.bullet)


    def run(self):
        self.start()
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.update()
            self.draw1()
            print(Settings.punkte)
        pygame.quit()


    def update(self):
        self.frontground.update()
        self.alien.update()
        self.bullet.update()
        self.all_bullets.update()
        self.check_for_collision()
        self.watch_for_events()
        self.gameover()

    
    def start(self):
        for a in range(Settings.nof_bullets):
            self.all_bullets.add(Bullet())
            
    def gameover(self):
        if Settings.lives==0:
            Settings.punkte = 0


    def check_for_collision(self):
        self.alien.hit = False
        for s in self.all_bullets:
            if pygame.sprite.collide_mask(s,self.alien):
                self.alien.hit = True
                break
        if self.alien.hit:
             self.alien.rect.top =600
             self.alien.rect.left=250
             if Settings.lives > 0:
                Settings.lives -=1
                
    def draw1(self):
        self.background.draw(self.screen)
        self.alien.draw(self.screen)
        self.all_bullets.draw(self.screen)
        self.bullet.draw(self.screen)
        self.frontground.draw(self.screen)
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
