import os, sys, random, pygame


pygame.init()
color = [0, 0, 0]
size = w, h = [900, 720]
screen = pygame.display.set_mode(size)
FPS = 60
n = 0
score = 0
sii = []
clock = pygame.time.Clock()
r = True
runny = True
lob = True



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

class Lobby():
    def __init__(self):
        super().__init__()
        self.bg = pygame.image.load("img/bg2.png")
        bg = pygame.transform.scale(self.bg, size)
        screen.blit(bg, (0, 0))
        self.WHITE, self.BLACK, self.GRAY = (255, 255, 255), (0, 0, 0), (128, 128, 128)
        self.font = pygame.font.Font(None, 50)
        self.button_width = 200
        self.button_height = 50
        self.button_x = w // 2 - self.button_width // 2
        self.button_y1 = h // 2 - self.button_height // 2 - 50
        self.button_y2 = h // 2 - self.button_height // 2 + 50
        self.button_y3 = h // 2 - self.button_height // 2 + 150
        self.start_button = pygame.Rect(w // 2 - self.button_width // 2, h // 2 - self.button_height // 2 - 50, 200, 50)
        self.exit_button = pygame.Rect(w // 2 - self.button_width // 2, h // 2 - self.button_height // 2 + 50, 200, 50)
        self.syst_button = pygame.Rect(w // 2 - self.button_width // 2, h // 2 - self.button_height // 2 + 150, 200, 50)
        self.scenescur = None
        self.scene1()
        while self.scenescur is not None:
            self.scenescur()

    def swiftscene(self, scene):
        self.scenescur = scene

    def scene1(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.swiftscene(None)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.start_button.collidepoint(event.pos):
                            self.swiftscene(self.scene2)
                            run = False
                        elif self.exit_button.collidepoint(event.pos):
                            run = False
                            self.swiftscene(None)
                        elif self.syst_button.collidepoint(event.pos):
                            run = False
                            self.swiftscene(self.scene2)
            screen.fill(self.WHITE)
            screen.blit(self.bg, (0, 0))
            pygame.draw.rect(screen, self.GRAY, self.start_button)
            pygame.draw.rect(screen, self.GRAY, self.exit_button)
            pygame.draw.rect(screen, self.GRAY, self.syst_button)
            start_text = self.font.render('Начать игру', True, self.BLACK)
            exit_text = self.font.render('Выход', True, self.BLACK)
            syst_text = self.font.render('Настройки', True, self.BLACK)
            screen.blit(start_text, (self.button_x + self.button_width // 2 - start_text.get_width() // 2,
                                     self.button_y1 + self.button_height // 2 - start_text.get_height() // 2))
            screen.blit(exit_text, (self.button_x + self.button_width // 2 - exit_text.get_width() // 2,
                                    self.button_y2 + self.button_height // 2 - exit_text.get_height() // 2))
            screen.blit(syst_text, (self.button_x + self.button_width // 2 - syst_text.get_width() // 2,
                                    self.button_y3 + self.button_height // 2 - syst_text.get_height() // 2))
            pygame.display.flip()

    def scene2(self):
        global lob
        lob = False


    def scene3(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.swiftscene(None)
            screen.fill(self.WHITE)
            pygame.display.flip()



all_sprites = pygame.sprite.Group()


class Bird(pygame.sprite.Sprite):
    image = load_image('img/'+ "ttt.png")
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bird.image
        self.rect = self.image.get_rect()
        self.wi, self.hi = self.image.get_size()
        self.rect.x = 0
        self.rect.y = 400
        self.v = 5

    def update(self, s=0):
        global score
        print(self.rect.x, self.rect.y, score)
        if s == 1:
            if self.rect.y == 0:
                pass
            else:
                self.rect.y -= self.v
        else:
            self.rect.y += self.v
        if self.rect.y >= h - self.wi:
            global runny
            runny = False
        if self.rect.x < (w - self.wi) // 3:
            self.rect.x += self.v
        self.map()
        for si in sii:
            if self.rect.colliderect(si):
                runny = False

    def map(self):
        if len(sii) == 0 or sii[len(sii) - 1].x < w - 200:
            sii.append(pygame.Rect(w + 50, 0, 50, 200))
            sii.append(pygame.Rect(w + 50, h - 201, 50,  200))


if __name__ == "__main__":
    Lobby()
    while lob:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lob = False
                r = False
                runny = False
        clock.tick(FPS)
        pygame.display.flip()
    Bird(all_sprites)
    while r:
        ok = 0
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = False
        if (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and runny:
            all_sprites.update(1)
            ok = 1
        background_image = pygame.image.load('img/bg.png')
        background_image = pygame.transform.scale(background_image, size)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        f1 = pygame.font.Font(None, 30 )
        text1 = f1.render(f'Score: {int(score)}', True,
                          (180, 0, 0))
        screen.blit(text1, (0, 0))
        if runny:
            if ok == 0:
                all_sprites.update()
            for si in sii:
                pygame.draw.rect(screen, pygame.Color('green'), si)
            for _ in range(len(sii) - 1, -1, -1):
                si = sii[_]
                si.x -= 5
                if si.x == 300:
                    score += 0.5
                if si.x + 50 < 0:
                    sii.remove(si)
        if not runny:
            f2 = pygame.font.Font(None, 160)
            text2 = f2.render('Wasted', True,
                              (180, 0, 0))
            screen.blit(text2, (w // 2, h // 2))
        clock.tick(FPS)
        pygame.display.flip()