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
run = True
runny = True


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
    image = load_image('img/' + "test4.png")
    image = pygame.transform.scale(image, (4 * qu, qu))
    bird = load_image('img/' + "ttt.png")
    bird = pygame.transform.scale(bird, (qu, qu))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bird.bird
        self.rect = self.image.get_rect()
        self.wi, self.hi = self.image.get_size()
        self.rect.x = 0
        self.rect.y = 400
        self.v = 7
        self.heighttonnel = Bird.qu * 3
        self.uptonnel = h // 2
        self.time = 0

    def update(self, s=0):
        global score
        if s == 1:
            if self.rect.y <= 0:
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
        self.time += 0.2
        if int(self.time) % 5 == 0:
            self.time = 1

        self.image = Bird.image.subsurface(int(self.time - 1) * Bird.qu, 0, 60, 60)
        screen.blit(self.image, self.rect)
        for si in sii:
            if self.rect.colliderect(si):
                runny = False

    def map(self):
        if len(sii) == 0 or sii[len(sii) - 1].x < w - 300:
            sii.append(pygame.Rect(w + 50, 0, 52, self.uptonnel - self.heighttonnel // 2))
            sii.append(pygame.Rect(w + 50, self.uptonnel + self.heighttonnel // 2, 52,
                                   h - self.uptonnel + self.heighttonnel // 2))
            ew = random.randint(-200, 200)
            self.uptonnel += ew
            if self.uptonnel < self.heighttonnel:
                self.uptonnel = self.heighttonnel
            elif self.uptonnel > h - self.heighttonnel:
                self.uptonnel = h - self.heighttonnel


if __name__ == "__main__":
    Bird(all_sprites)
    while run:
        ok = 0
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and runny:
            all_sprites.update(1)
            ok = 1
        background_image = pygame.image.load('img/bg.png')
        background_image = pygame.transform.scale(background_image, size)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        cdown = load_image('img/' + 'colonaDAWN.png')
        cup = load_image('img/' + 'colonaUP.png')
        if runny:
            if ok == 0:
                all_sprites.update()
            for si in sii:
                if si.y == 0:
                    rect = cup.get_rect(bottomleft=si.bottomleft)
                    screen.blit(cup, rect)
                else:
                    rect = cdown.get_rect(topleft=si.topleft)
                    screen.blit(cdown, rect)
            for _ in range(len(sii) - 1, -1, -1):
                si = sii[_]
                si.x -= 5
                if si.x == 300:
                    score += 0.5
                if si.x + 50 < 0:
                    sii.remove(si)
        if not runny:
            f1 = pygame.font.Font(None, 100)
            text1 = f1.render(f'Score: {int(score)}', True,
                          (180, 0, 0))
            screen.blit(text1, (w//2, h//2 - 100))
            f2 = pygame.font.Font(None, 160)
            text2 = f2.render('Wasted', True,
                              (180, 0, 0))
            screen.blit(text2, (w // 2, h // 2))
        clock.tick(FPS)
        pygame.display.flip()