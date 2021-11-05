import pygame as pg


class settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.ship_limit = 3
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
class sprite(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.screen_rect = self.screen.get_rect()

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        elif self.rect.top <= 0:
            return True
        elif self.rect.bottom >= screen_rect.bottom:
            return True
        else:
            return False

    def update(self):
        self.rect.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        if self.check_edges():
            self.settings.fleet_direction *= -1
            self.rect.y += self.settings.fleet_drop_speed
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(pg.Color("blue"))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.vx, self.vy = 0, 0
        self.speed = 1
    
    def move(self):
        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed
        if self.rect.left <= 0:
            self.rect.left = 0

class meteor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((self.game.settings.bullet_width, self.game.settings.bullet_height))
        self.image.fill(pg.Color("yellow"))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.vx, self.vy = 0, 0
        self.speed = self.game.settings.bullet_speed_factor

    def update(self):
        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed
        if self.rect.right > self.game.screen_rect.right:
            self.kill()
        if self.rect.left < self.game.screen_rect.left:
            self.kill()
        if self.rect.bottom > self.game.screen_rect.bottom:
            self.kill()
        if self.rect.top < self.game.screen_rect.top:
            self.kill()

class game (pg.sprite.Sprite):
    def __init__(self):
        self.settings = settings()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        self.bg_color = self.settings.bg_color
        self.bg_color = pg.Color(self.bg_color)
        self.screen_rect = self.screen.get_rect()
        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = Player(self)
        self.game_active = False
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont(None, 48)

    def run_game(self):
        self.game_active = True
        while self.game_active:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
            
    def update(self):
        self.all_sprites.update()
        self.bullets.update()
        self.player.move()

    def draw(self):
        self.screen.fill(self.bg_color)
        self.all_sprites.draw(self.screen)
        self.bullets.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.player.image, self.player.rect)
        pg.display.flip()


