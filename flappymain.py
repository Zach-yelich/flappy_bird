import  pygame, sys

pygame.init()
screen = pygame.display.set_mode((576, 1024))
Clock = pygame.time.Clock()

bg_surface = pygame.image.load('downloads/assests/background-day.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg_surface(0,0))

    pygame.display.update()
    Clock.tick(120)
