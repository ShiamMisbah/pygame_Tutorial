import pygame
from os.path import join
from random import randint, uniform

# class PlayerAnimation (pygame.sprite.Sprite):
#     def __init__(self, frames, pos, groups):
#         super().__init__(groups)
#         self.frames = frames
#         self.frame_index = 0
#         self.image = frames[self.frame_index]
#         self.rect = self.image.get_frect(center = pos)

#     def update(self, dt):
#         self.rect.center = player.rect.center
#         self.frame_index += 20 * dt
#         self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Player(pygame.sprite.Sprite):
    def __init__(self, frames, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 300
        self.rotation = 0

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400



    # def __init__(self, groups) :
    #     super().__init__(groups)
    #     self.original_surface = pygame.image.load(path+'/player.png').convert_alpha()
    #     self.image = self.original_surface
    #     self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
    #     self.direction = pygame.math.Vector2(0,0)
    #     self.speed = 300
    #     self.rotation = 0

    #     # cooldown
    #     self.can_shoot = True
    #     self.laser_shoot_time = 0
    #     self.cooldown_duration = 400

    #     # mask
    #     self.mask = pygame.mask.from_surface(self.image)


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
            # Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            BulletAnimation(bullet_frames, (player.rect.midtop), (all_sprites, laser_sprites))
            laser_sound.play()
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()
        if (self.rect.left < 0):
            self.rect.left = 0
        elif (self.rect.right > WINDOW_WIDTH):
            self.rect.right = WINDOW_WIDTH
        elif (self.rect.top < 0):
            self.rect.top = 0
        elif (self.rect.bottom > WINDOW_HEIGHT):
            self.rect.bottom = WINDOW_HEIGHT   
        else:
            self.rect.center += self.direction * self.speed * dt
        
        self.frame_index += 20 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        # mask
        self.mask = pygame.mask.from_surface(self.image )
        # continuous transform test
        # self.rotation += 100*dt
        # self.image = pygame.transform.rotozoom(self.original_surface, self.rotation, 1)
        

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
        self.mask = pygame.mask.from_surface(self.image)

    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surface = surf
        self.image = self.original_surface
        self.rect = self.image.get_frect(center = pos)
        self.born_time = pygame.time.get_ticks()
        self.duration = 2000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400, 500)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation = 0
        self.rotation_speed = randint(40,80)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        current_time = pygame.time.get_ticks()
        if current_time - self.born_time >= self.duration:
            self.kill()
        
        # continuous transform test
        self.rotation += self.rotation_speed*dt
        self.image = pygame.transform.rotozoom(self.original_surface, self.rotation, 0.5)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

class BulletAnimation (pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
        self.frame_index += 20 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]



def collisions():
    global running
    collided_sprite = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collided_sprite:
        damage_sound.play()
        running = True
    for laser in laser_sprites:
        collided_sprite = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprite:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()


def display_score():
    current_time = pygame.time.get_ticks()//1000
    text_surf = font.render(str(current_time), True, (240,240,240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(20,20).move(0, -8), 2, 5)


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 720, 900
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()
path = join('Game1','images')





# importing image
star_surf = pygame.image.load(path+'/star.png').convert_alpha()
meteor_surf = pygame.image.load(path+'/meteor.png')
laser_surf = pygame.image.load(path+'/laser.png')
font = pygame.font.Font(path+'/Oxanium-Bold.ttf', 40)
explosion_frames = [pygame.image.load(join(path, 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
player_frames = [pygame.image.load(join(path, 'bara', f'{i}.png')).convert_alpha() for i in range(5)]
bullet_frames = [pygame.image.load(join(path, 'maal', f'sprite_maal{i}.png')).convert_alpha() for i in range(6)]
meteor_frames = [pygame.image.load(join(path, 'meteor', f'{i}.png')).convert_alpha() for i in range(5)]

laser_sound = pygame.mixer.Sound(join('Game1', 'audio', 'laser.wav'))
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(join('Game1', 'audio', 'explosion.wav'))
explosion_sound.set_volume(0.1)
damage_sound = pygame.mixer.Sound(join('Game1', 'audio', 'damage.ogg'))
damage_sound.set_volume(0.3)
game_music = pygame.mixer.Sound(join('Game1', 'audio', 'game_music.wav'))
game_music.set_volume(0.2)
game_music.play(loops=-1)


# All sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(player_frames, all_sprites)

# custom event --> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_frames[randint(0, len(meteor_frames)-1)], (randint(0, WINDOW_WIDTH - meteor_surf.get_width()), randint(-200, -100)), (all_sprites, meteor_sprites))

    all_sprites.update(dt)
    collisions()


    # draw the game
    display_surface.fill('#3a2e3f')
    all_sprites.draw(display_surface)
    display_score()

    # draw test


    pygame.display.update()

pygame.quit()