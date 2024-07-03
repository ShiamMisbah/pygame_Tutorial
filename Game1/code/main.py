import pygame

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

# Surface
surf = pygame.Surface((1100,600))
surf2 = pygame.Surface((50,50))
surf2.fill('blue')
x=0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x += 1
    # draw the game
    display_surface.fill('darkgray')
    surf.fill('white')
    surf.blit(surf2, ((x,0)))
    display_surface.blit(surf, ((10,50)))
    

    pygame.display.update()

pygame.quit()