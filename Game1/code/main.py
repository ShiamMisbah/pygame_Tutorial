import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups) :
        super().__init__(groups)
        self.image = pygame.image.load(path+'/player.png').convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()
        # self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
        self.rect.center += self.direction * self.speed * dt

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.born_time = pygame.time.get_ticks()
        self.duration = 2000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400, 500)
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        current_time = pygame.time.get_ticks()
        if current_time - self.born_time >= self.duration:
            self.kill()

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()
path = join('Game1','images')

all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(path+'/star.png').convert_alpha()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)



# importing image
meteor_surf = pygame.image.load(path+'/meteor.png')
laser_surf = pygame.image.load(path+'/laser.png')

# custom event --> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, (randint(0, WINDOW_WIDTH - meteor_surf.get_width()), randint(-200, -100)), all_sprites)

    all_sprites.update(dt)

    # draw the game
    display_surface.fill('darkgray')
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()