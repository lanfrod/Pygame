import pygame, os, sys, random

pygame.init()

WIDTH = 900
HEIGHT = 720
BackGround = pygame.image.load("img/bg.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (128, 128, 128)
font = pygame.font.Font(None, 50)

button_width = 200
button_height = 50

button_x = WIDTH // 2 - button_width // 2

button_y1 = HEIGHT // 2 - button_height // 2 - 50
button_y2 = HEIGHT // 2 - button_height // 2 + 50
button_y3 = HEIGHT // 2 - button_height // 2 + 150

button_newgame = HEIGHT // 2 - button_height // 2 - 50
button_menu = HEIGHT // 2 - button_height // 2 + 50
start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 - 50, 200, 50)
exit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 + 50, 200, 50)
syst_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 + 150, 200, 50)
NewGame_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 - 50, 200, 50)
menu_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 + 50, 200, 50)
scenescur = None
running = True


def swiftscene(scene):
    global scenescur
    scenescur = scene


def scene1(skin=1, bg=1):
    run1 = True
    while run1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run1 = False
                swiftscene(None)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.collidepoint(event.pos):
                        swiftscene(scene2(skin))
                        run1 = False
                    elif exit_button.collidepoint(event.pos):
                        run1 = False
                        swiftscene(None)
                    elif syst_button.collidepoint(event.pos):
                        swiftscene(scene3())
                        run1 = False

        screen.fill(WHITE)
        screen.blit(BackGround, (0, 0))
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


all_sprites = pygame.sprite.Group()


def scene2(cnt):
    pygame.init()
    size = w, h = [900, 720]
    screen = pygame.display.set_mode(size)
    FPS = 60
    score = 0
    sii = []
    clock = pygame.time.Clock()
    run = True
    rec = True

    def load_image(name, colorkey=None):
        fullname = os.path.join(name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    all_sprites = pygame.sprite.Group()

    class Bird(pygame.sprite.Sprite):
        qu = 60

        image = load_image(f'img/birdews{cnt}.png')
        image = pygame.transform.scale(image, (4 * qu, qu))

        def __init__(self, *group):
            super().__init__(*group)
            self.image = Bird.image.subsurface(0, 0, 60, 60)
            self.rect = self.image.get_rect()
            self.wi, self.hi = self.image.get_size()
            self.rect.x = 0
            self.rect.y = 0
            self.bird_speed = 7
            self.height_tunnel = Bird.qu * 3
            self.upper_tunnel = h // 2
            self.time = 0
            self.k = 0
            self.flag = False
            self.rot = 0

        def update(self, s=0):
            global score, running
            if s != self.flag:
                self.k = 0
                self.flag = not self.flag
            if not running:
                if self.rot <= 25:
                    self.rot += 1
                    self.rect.y -= self.bird_speed
                elif self.rot > 25:
                    self.rect.y += self.bird_speed
                # angle = 5
                self.image = pygame.transform.rotate(self.image, 1)
            elif s == 1:
                if self.rect.y <= 0:
                    pass
                else:
                    self.rect.y -= self.bird_speed
                if self.k < 90:
                    self.k += 1
            else:
                self.rect.y += self.bird_speed
                if self.k > -90:
                    self.k -= 1
            if self.rect.y >= h - self.wi:
                running = False
            if self.rect.x < (w - self.wi) // 3:
                self.rect.x += self.bird_speed
            if running:
                self.map()
                self.time += 0.2
                if int(self.time) % 5 == 0:
                    self.time = 1
                self.image = Bird.image.subsurface(int(self.time - 1) * Bird.qu, 0, 60, 60)
                self.image = pygame.transform.rotate(self.image, int(self.k))
            for si in sii:
                if self.rect.colliderect(si):
                    running = False

        def map(self):
            if len(sii) == 0 or sii[len(sii) - 1].x < w - 300:
                sii.append(pygame.Rect(w + 50, 0, 52, self.upper_tunnel - self.height_tunnel // 2))
                sii.append(pygame.Rect(w + 50, self.upper_tunnel + self.height_tunnel // 2, 52,
                                       h - self.upper_tunnel + self.height_tunnel // 2))
                ew = random.randint(-200, 200)
                self.upper_tunnel += ew
                if self.upper_tunnel < self.height_tunnel:
                    self.upper_tunnel = self.height_tunnel
                elif self.upper_tunnel > h - self.height_tunnel:
                    self.upper_tunnel = h - self.height_tunnel

    if __name__ == "__main__":
        Bird(all_sprites)
        try:
            with open('best.txt', 'r') as file:
                record = float(file.read().split('\n')[0])
        except:
            record = 0
        print(record)
        while run:
            ok = 0
            pygame.init()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    swiftscene(None)
                    global running
                elif event.type == pygame.MOUSEBUTTONDOWN and not running:
                    if NewGame_button.collidepoint(event.pos):
                        running = True
                        run = False
                        swiftscene(scene2(cnt))
                    elif menu_button.collidepoint(event.pos):
                        running = True
                        run = False
                        swiftscene(scene1())
            if (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and running:
                all_sprites.update(1)
                ok = 1
            background_image = pygame.image.load('img/bg2.png')
            background_image = pygame.transform.scale(background_image, size)
            screen.blit(background_image, (0, 0))
            all_sprites.draw(screen)
            cdown = load_image('img/' + 'colonaDAWN.png')
            cup = load_image('img/' + 'colonaUP.png')
            if running:
                if ok == 0:
                    all_sprites.update()
                for si in sii:
                    if si.y == 0:
                        rect = cup.get_rect(bottomleft=si.bottomleft)
                        screen.blit(cup, rect)
                    else:
                        rect = cdown.get_rect(topleft=si.topleft)
                        screen.blit(cdown, rect)
                # colons speed
                for _ in range(len(sii) - 1, -1, -1):
                    si = sii[_]
                    si.x -= 5
                    if si.x == 300:
                        score += 0.5
                    if si.x + 50 < 0:
                        sii.remove(si)
            if not running:
                all_sprites.update()
                if score > record and rec:
                    with open('best.txt', 'w') as file: file.write(str(int(score)))
                    f2 = pygame.font.Font(None, 60)
                    text2 = f2.render(f'Новый рекорд!', True, 'blue')
                    screen.blit(text2, (w // 2, h // 2))
                f1 = pygame.font.Font(None, 100)
                text1 = f1.render(f"Счёт: {int(score)}", True,
                                  'green')
                screen.blit(text1, (w // 2, h // 2 - 100))
                pygame.draw.rect(screen, GRAY, NewGame_button)
                pygame.draw.rect(screen, GRAY, menu_button)

                newgame_text = font.render('Новая игра', True, BLACK)
                screen.blit(newgame_text, (button_x + button_width // 2 - newgame_text.get_width() // 2,
                                           button_y1 + button_height // 2 - newgame_text.get_height() // 2))
                menu_text = font.render('Меню', True, BLACK)
                screen.blit(menu_text, (button_x + button_width // 2 - menu_text.get_width() // 2,
                                        button_y2 + button_height // 2 - menu_text.get_height() // 2))
            clock.tick(FPS)
            pygame.display.flip()


def scene3():
    run = True
    first_skin = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 - 50, 200, 50)
    second_skin = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2 + 50, 200, 50)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                swiftscene(None)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if first_skin.collidepoint(event.pos):
                        swiftscene(scene1(1))
                        run = False
                    elif second_skin.collidepoint(event.pos):
                        run = False
                        swiftscene(scene1(2))
        screen.fill(WHITE)
        first_text = font.render('1', True, BLACK)
        second_text = font.render('2', True, BLACK)
        screen.blit(first_text, (button_x + button_width // 2 - first_text.get_width() // 2,
                                 button_y1 + button_height // 2 - first_text.get_height() // 2))
        screen.blit(second_text, (button_x + button_width // 2 - second_text.get_width() // 2,
                                  button_y2 + button_height // 2 - second_text.get_height() // 2))
        pygame.display.flip()


swiftscene(scene1)
while scenescur is not None:
    scenescur()

pygame.quit()
