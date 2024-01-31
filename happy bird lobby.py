import pygame

pygame.init()

WIDTH = 900
HEIGHT = 504
bg = pygame.image.load("rtrtrtt.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (128, 128, 128)
font = pygame.font.Font(None, 50)
button_width = 200
button_height = 50
button_x = WIDTH // 2 - button_width // 2
button_y1 = HEIGHT // 2 - button_height // 2 - 50
button_y2 = HEIGHT // 2 - button_height // 2 + 50
button_y3 = HEIGHT // 2 - button_height // 2 + 150
start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 - 50, 200, 50)
exit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 + 50, 200, 50)
syst_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 + 150, 200, 50)
scenescur = None


def swiftscene(scene):
    global scenescur
    scenescur = scene


def scene1():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                swiftscene(None)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.collidepoint(event.pos):
                        swiftscene(scene2)
                        run = False
                    elif exit_button.collidepoint(event.pos):
                        run = False
                        swiftscene(None)
                    elif syst_button.collidepoint(event.pos):
                        run = False
                        swiftscene(scene2)
        screen.fill(WHITE)
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, GRAY, start_button)
        pygame.draw.rect(screen, GRAY, exit_button)
        pygame.draw.rect(screen, GRAY, syst_button)
        start_text = font.render('Начать игру', True, BLACK)
        exit_text = font.render('Выход', True, BLACK)
        syst_text = font.render('Настройки', True, BLACK)
        screen.blit(start_text, (button_x + button_width // 2 - start_text.get_width() // 2,
                                 button_y1 + button_height // 2 - start_text.get_height() // 2))
        screen.blit(exit_text, (button_x + button_width // 2 - exit_text.get_width() // 2,
                                button_y2 + button_height // 2 - exit_text.get_height() // 2))
        screen.blit(syst_text, (button_x + button_width // 2 - syst_text.get_width() // 2,
                                button_y3 + button_height // 2 - syst_text.get_height() // 2))
        pygame.display.flip()


def scene2():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                swiftscene(None)
        screen.fill(WHITE)
        pygame.display.flip()


def scene3():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                swiftscene(None)
        screen.fill(WHITE)
        pygame.display.flip()

swiftscene(scene1)
while scenescur is not None:
    scenescur()

pygame.quit()