from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites


from random import randint

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Bacha Morar Lorai')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        map = load_pygame(join('Game2', 'data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x,obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x,obj.y), pygame.Surface((obj.width, obj.height)), (self.collision_sprites))
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)

    def draw_collision_border_player(self, obj):
        # Draw a red border around the player's hitbox_rect
        offset_x = obj.hitbox_rect.x + self.all_sprites.offset.x
        offset_y = obj.hitbox_rect.y + self.all_sprites.offset.y
        offset_rect = pygame.Rect(offset_x, offset_y, obj.hitbox_rect.width, obj.hitbox_rect.height)
        pygame.draw.rect(self.display_surface, 'red', offset_rect, 2)

    def draw_collision_border(self, obj):
        # Draw a red border around the player's hitbox_rect
        offset_x = obj.rect.x + self.all_sprites.offset.x
        offset_y = obj.rect.y + self.all_sprites.offset.y
        offset_rect = pygame.Rect(offset_x, offset_y, obj.rect.width, obj.rect.height)
        pygame.draw.rect(self.display_surface, 'red', offset_rect, 2)

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)

            # collosion border
            # self.draw_collision_border_player(self.player)  # Draw the collision border
            # for sprite in self.collision_sprites:
            #     if not hasattr(sprite, 'ground'):
            #         self.draw_collision_border(sprite)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()