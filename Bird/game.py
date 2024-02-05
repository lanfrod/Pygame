import pygame_widgets
import pygame, os, sys, random
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()
re = 50
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


def lobby(skin=1, bg=1):
    run1 = True
    while run1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run1 = False
                swiftscene(None)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button.collidepoint(event.pos):
                        swiftscene(game(skin))
                        run1 = False
                    elif exit_button.collidepoint(event.pos):
                        run1 = False
                        swiftscene(None)
                    elif syst_button.collidepoint(event.pos):
                        swiftscene(settings())
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


def game(num_skin):
    pygame.init()
    size = w, h = [900, 720]
    screen = pygame.display.set_mode(size)
    FPS = 60
    score = 0
    flag_hard = True
    coloms = []
    clock = pygame.time.Clock()
    run = True
    rec_flag = True

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

        image = load_image(f'img/birdews{num_skin}.png')
        image = pygame.transform.scale(image, (4 * qu, qu))

        def __init__(self, *group):
            super().__init__(*group)
            self.image = Bird.image.subsurface(0, 0, 60, 60)
            self.rect = self.image.get_rect()
            self.weight_im, self.height_im = self.image.get_size()
            self.rect.x = 0
            self.rect.y = 0
            self.bird_speed = 7
            self.height_tunnel = Bird.qu * 3
            self.upper_tunnel = h // 2
            self.time = 0
            self.k = 0
            self.flag = False
            self.time_rotation = 0
            self.diesound_flag = True
            self.hitsound_flag = True
            self.flag_score = True

        def update(self, s=0):
            global running
            if s != self.flag and s == 1:
                upsound.play()
            if s != self.flag:
                self.k = 0
                self.flag = not self.flag
            if not running:
                if self.time_rotation <= 25:
                    self.time_rotation += 1
                    self.rect.y -= self.bird_speed
                elif self.time_rotation > 25:
                    self.rect.y += self.bird_speed
                if self.time_rotation > 25 and self.diesound_flag:
                    self.diesound_flag = False
                    diesound.play()
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
            if self.rect.y >= h - self.weight_im:
                running = False
                if self.hitsound_flag:
                    hitsound.play()
                    self.hitsound_flag = False
            if self.rect.x < (w - self.weight_im) // 3:
                self.rect.x += self.bird_speed
            if score % 10 != 0:
                self.flag_score = True
            if score % 10 == 0 and score != 0 and self.flag_score and self.height_tunnel > 120:
                self.height_tunnel -= 5
                self.flag_score = False
            if running:
                self.map()
                self.time += 0.2
                if int(self.time) % 5 == 0:
                    self.time = 1
                self.image = Bird.image.subsurface(int(self.time - 1) * Bird.qu, 0, 60, 60)
                self.image = pygame.transform.rotate(self.image, int(self.k))
            for si in coloms:
                if self.rect.colliderect(si):
                    running = False
                    if self.hitsound_flag:
                        hitsound.play()
                        self.hitsound_flag = False

        def map(self):
            if len(coloms) == 0 or coloms[len(coloms) - 1].x < w - 300:
                coloms.append(pygame.Rect(w + 50, 0, 52, self.upper_tunnel - self.height_tunnel // 2))
                coloms.append(pygame.Rect(w + 50, self.upper_tunnel + self.height_tunnel // 2, 52,
                                       h - self.upper_tunnel + self.height_tunnel // 2))
                size_tonnel = random.randint(-200, 200)
                self.upper_tunnel += size_tonnel
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
        while run:
            upsound = pygame.mixer.Sound('sounds/Wing.wav')
            pointsound = pygame.mixer.Sound('sounds/Point.wav')
            hitsound = pygame.mixer.Sound('sounds/Hit.wav')
            diesound = pygame.mixer.Sound('sounds/Die.wav')
            upsound.set_volume(re / 100)
            pointsound.set_volume(re / 100)
            hitsound.set_volume(re / 100)
            diesound.set_volume(re / 100)
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
                        swiftscene(game(num_skin))
                    elif menu_button.collidepoint(event.pos):
                        running = True
                        run = False
                        swiftscene(lobby(num_skin))
            if (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and running:
                all_sprites.update(1)
                ok = 1
            background_image = pygame.image.load('img/bg.png')
            background_image = pygame.transform.scale(background_image, size)
            screen.blit(background_image, (0, 0))
            all_sprites.draw(screen)
            cdown = load_image('img/' + 'colonaDAWN.png')
            cup = load_image('img/' + 'colonaUP.png')
            if running:
                f3 = pygame.font.Font(None, 40)
                text3 = f3.render(f"Счёт: {int(score)}", True,
                                  'green')
                screen.blit(text3, (0, 0))
                if ok == 0:
                    all_sprites.update()
                for si in coloms:
                    if si.y == 0:
                        rect = cup.get_rect(bottomleft=si.bottomleft)
                        screen.blit(cup, rect)
                    else:
                        rect = cdown.get_rect(topleft=si.topleft)
                        screen.blit(cdown, rect)
                # colons speed
                for _ in range(len(coloms) - 1, -1, -1):
                    si = coloms[_]
                    si.x -= 5
                    if si.x == 300:
                        score += 0.5
                        pointsound.play()
                    if si.x + 50 < 0:
                        coloms.remove(si)
            if not running:
                all_sprites.update()
                if score > record and rec_flag:
                    with open('best.txt', 'w') as file: file.write(str(int(score)))
                    f2 = pygame.font.Font(None, 60)
                    text2 = f2.render(f'Новый рекорд!', True, 'blue')
                    screen.blit(text2, (w // 2 - 150, 150))
                f1 = pygame.font.Font(None, 100)
                text1 = f1.render(f"Счёт: {int(score)}", True,
                                  'green')
                screen.blit(text1, (w // 2 - 115, 200))
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


def settings():
    global re
    cnt = 1
    time = 0
    run = True
    first_skin = pygame.Rect(WIDTH // 2 - button_width // 2 - 100, HEIGHT // 2 - button_height // 2 - 50, 100, 100)
    second_skin = pygame.Rect(WIDTH // 2 + button_width // 2, HEIGHT // 2 - button_height // 2 - 50, 100, 100)
    exit = pygame.Rect(WIDTH // 2 - button_width // 2 + 50, HEIGHT // 2 + 200, 100, 30)
    sli = Slider(screen, 250, 100, 400, 40, min=1, max=100, step=1)
    sli.setValue(re)
    output = TextBox(screen, 425, 175, 50, 50, fontSize=30)
    output.disable()  # Act as label instead of textbox
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                swiftscene(None)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if first_skin.collidepoint(event.pos):
                        cnt -= 1
                        if cnt == 0:
                            cnt = 3
                    elif second_skin.collidepoint(event.pos):
                        cnt += 1
                        if cnt == 4:
                            cnt = 1
                    elif exit.collidepoint(event.pos):
                        sli.hide()
                        run = False
                        swiftscene(lobby(cnt))
        background_image = pygame.image.load('img/bg.png')
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(background_image, (0, 0))
        time += 0.1
        if int(time) % 5 == 0:
            time = 1
        re = sli.getValue()
        output.setText(re)
        pygame_widgets.update(events)
        image = pygame.image.load(f'img/birdews{cnt}.png')
        image = pygame.transform.scale(image, (480, 120))
        image = image.subsurface((int(time) - 1) * 120, 0, 120, 120)
        screen.blit(image, (WIDTH // 2 - button_width // 2 + 35, HEIGHT // 2 - button_height // 2 - 70))
        first_text = font.render('Меню', True, BLACK)
        screen.blit(first_text, (WIDTH // 2 - button_width // 2 + 50, HEIGHT // 2 + 200))
        left_ar = pygame.image.load('img/strelr.png')
        left_ar = pygame.transform.scale(left_ar, (100, 100))
        screen.blit(left_ar, (WIDTH // 2 - button_width // 2 - 100, HEIGHT // 2 - button_height // 2 - 50))
        right_ar = pygame.image.load('img/strell.png')
        right_ar = pygame.transform.scale(right_ar, (100, 100))
        screen.blit(right_ar, (WIDTH // 2 + button_width // 2, HEIGHT // 2 - button_height // 2 - 50))
        pygame.display.flip()


swiftscene(lobby)
while scenescur is not None:
    scenescur()

pygame.quit()
