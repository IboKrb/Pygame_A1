import pygame
import os
from random import randint


# steuerung mit pfeiltasten

class Settings:  # Settigns einstellung mit allen variabel für programmieren
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
    nof_bullets = 4
    punkte = 0
    punkte2 = 0
    heart_width = 80
    heart_height = 60
    lives = 3


class Front(pygame.sprite.Sprite):  # klasse Frontground alle schriften bilder die im vordergrund sind
    def __init__(self) -> None:  # initaliziert
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, "heart.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.heart_width, Settings.heart_height))

    def draw(self, screen):  # im fenster dastellen
        screen.blit(self.image, (480, 730))

        punkte = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        punktetxt = punkte.render(f"Punkte:{Settings.punkte}", 1, (0, 0, 0))
        screen.blit(punktetxt, (30, 20))

        lives = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        livestxt = lives.render(f"x{Settings.lives}", 1, (255, 255, 255))
        screen.blit(livestxt, (530, 750))


class Gameover(pygame.sprite.Sprite):  # klasse Gameover wenn spiel verloren ist
    def __init__(self) -> None:
        super().__init__()

    def draw(self, screen):  # im fenster dastellen
        gameover = pygame.font.SysFont(pygame.font.get_default_font(), 60)
        gameovertxt = gameover.render(f"Game over deine Punkte :{Settings.punkte2}", 5, (160, 2, 205))
        screen.blit(gameovertxt, (15, 400))

        gameover = pygame.font.SysFont(pygame.font.get_default_font(), 60)
        gameovertxt = gameover.render(f"Drück R um weiter zu spielen", 5, (39, 100, 100))
        screen.blit(gameovertxt, (5, 450))


class Background(pygame.sprite.Sprite):  # klasse background/ hintergrund
    def __init__(self, filename="background.png") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):  # im fenster dastellen
        screen.blit(self.image, (0, 0))


class Alien(pygame.sprite.Sprite):  # klasse alien
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

    def update(self):  # wand wird gesetzt vom spieler
        if self.rect.top >= Settings.window_height - 60:
            self.rect.top = Settings.window_height - 70
        if self.rect.left >= Settings.window_width - 50:
            self.rect.left = Settings.window_width - 50
        if self.rect.top <= 1:
            self.rect.top = 1
        if self.rect.left <= 1:
            self.rect.left = 1

    def draw(self, screen):  # im fenster dastellen
        screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):  # klasse bullet
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(Settings.path_image, "bullet.png")).convert_alpha()  # bullet wird eingefüht und converted

        scale_ratio = randint(1, 3) / 4
        self.image = pygame.transform.scale(self.image, (
            int(self.image.get_rect().width * scale_ratio),
            int(self.image.get_rect().height * scale_ratio)
        ))

        self.image = self.image
        self.rect = self.image.get_rect()
        self.speed_x = randint(1, 3)
        self.speed_y = randint(1, 3)

    def update(self):  # movment von bullet
        self.rect.move_ip(0, self.speed_x * self.speed_y)
        if self.rect.top >= Settings.window_height:
            self.rect.centerx = randint(0, Settings.window_width)
            self.rect.centery = randint(0, 10)
            Settings.punkte += 1

    def draw(self, screen):  # im fenster dastellen
        screen.blit(self.image, self.rect)


class Game(object):  # klasse game
    def __init__(self, ) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"

        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.front = Front()
        self.background = Background()
        self.bullet = Bullet()
        self.alien = Alien()
        self.gameover = Gameover()
        self.all_bullets = pygame.sprite.Group()
        self.all_bullets.add(self.bullet)
        self.zahl0 = 0
        self.zahl = 0
        self.zahl2 = 0
        self.zahl3 = 0
        self.zahl4 = 0

    def run(self):  # beim spiel start ausführen
        self.start()
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.update()
        pygame.quit()

    def update(self):  # alle funktionen werden in eine gesteckt
        self.draw1()
        self.alien.update()
        self.bullet.update()
        self.all_bullets.update()
        self.check_for_collision()
        self.watch_for_events()
        self.lost()
        self.punktespeichern()
        self.lvlupdate()

    def start(self):  # bullets werden erstelt
        for a in range(Settings.nof_bullets):
            self.all_bullets.add(Bullet())

    def lost(self):  # spiel verloren
        if Settings.lives == 0:
            Settings.punkte = 0
            self.alien.rect.top = 600
            self.alien.rect.left = 250
            for i in self.all_bullets.sprites():
                i.remove(self.all_bullets)

    def check_for_collision(self):  # collision und alliens beim hitten entfernen und spawnen
        self.bullet.hit = pygame.sprite.collide_mask(self.bullet,self.alien)
        self.alien.hit = False
        for s in self.all_bullets:
            if pygame.sprite.collide_mask(s, self.alien) or self.bullet.hit:
                self.alien.hit = True
                break
        if self.alien.hit:
            self.alien.rect.top = 600
            self.alien.rect.left = 250
            if Settings.lives > 0:
                Settings.lives -= 1
            for i in self.all_bullets.sprites():
                i.remove(self.all_bullets)
            if Settings.punkte >= 0:
                for a in range(Settings.nof_bullets):
                    self.all_bullets.add(Bullet())

    def lvlupdate(self):  # Schwierigkeits grad wird jenach punkten schneller und spawnt mehr
        if 0 <= Settings.punkte <= 30:
            self.bullet.speed_y += 1
            if self.bullet.speed_y >= 3:
                self.bullet.speed_y = 3
            Settings.nof_bullets += 1
            if Settings.nof_bullets > 4:
                Settings.nof_bullets = 4
                self.zahl0 += 1
            if self.zahl0 <= 1:
                self.all_bullets.add(Bullet())
        elif 30 <= Settings.punkte <= 50:  # lvl1
            self.bullet.speed_y += 1
            if self.bullet.speed_y >= 5:
                self.bullet.speed_y = 3
            Settings.nof_bullets += 1
            if Settings.nof_bullets > 8:
                Settings.nof_bullets = 7
                self.zahl += 1
            if self.zahl <= 1:
                self.all_bullets.add(Bullet())
        elif 50 <= Settings.punkte <= 70:  # lvl 2
            self.bullet.speed_y += 1
            if self.bullet.speed_y >= 8:
                self.bullet.speed_y = 6
            Settings.nof_bullets += 1
            if Settings.nof_bullets > 10:
                Settings.nof_bullets = 9
            self.zahl2 += 1
            if self.zahl2 <= 1:
                self.all_bullets.add(Bullet())
        elif 70 <= Settings.punkte <= 100:  # lvl 3
            self.bullet.speed_y += 1
            if self.bullet.speed_y >= 15:
                self.bullet.speed_y = 13
            Settings.nof_bullets += 1
            if Settings.nof_bullets > 12:
                Settings.nof_bullets = 11
            self.zahl3 += 1
            if self.zahl3 <= 1:
                self.all_bullets.add(Bullet())
        elif 100 <= Settings.punkte <= 130:  # lvl 4
            self.bullet.speed_y += 1
            if self.bullet.speed_y >= 18:
                self.bullet.speed_y = 17
            Settings.nof_bullets += 1
            if Settings.nof_bullets > 12:
                Settings.nof_bullets = 11
            self.zahl4 += 1
            if self.zahl4 <= 1:
                self.all_bullets.add(Bullet())

    def punktespeichern(self):  # zwischen speicher für punkte
        if Settings.punkte > 0:
            Settings.punkte2 = Settings.punkte

    def draw1(self):  # draw alle bitmaps in der funktion
        self.background.draw(self.screen)
        self.alien.draw(self.screen)
        self.all_bullets.draw(self.screen)
        self.bullet.draw(self.screen)
        self.front.draw(self.screen)
        if Settings.punkte == 0 and Settings.lives == 0:
            self.gameover.draw(self.screen)

        pygame.display.flip()

    def watch_for_events(self):  # steuerung
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
            if Settings.lives == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        Settings.lives = 3
                        self.all_bullets.add(Bullet())


if __name__ == '__main__':  # game start
    game = Game()
    game.run()
