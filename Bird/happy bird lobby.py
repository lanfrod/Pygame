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
    #name = ....
    #image = load_image(f'img/birdews{name}.png')
    image = load_image(f'img/birdews2.png')
    image = pygame.transform.scale(image, (4 * qu, qu))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bird.image.subsurface(0, 0, 60, 60)
        self.rect = self.image.get_rect()
        self.wi, self.hi = self.image.get_size()
        self.rect.x = 0
        self.rect.y = 400
        self.v = 7
        self.heighttonnel = Bird.qu * 3
        self.uptonnel = h // 2
        self.time = 0
        self.k = 0
        self.flag = False
        self.rot = 0

    def update(self, s=0):
        global score, runny
        if s != self.flag:
            self.k = 0
            self.flag = not self.flag
        if not runny:
            if self.rot <= 25:
                self.rot += 1
                self.rect.y -= self.v
            elif self.rot > 25:
                self.rect.y += self.v
            self.image = pygame.transform.rotate(self.image, 1)
        elif s == 1:
            if self.rect.y <= 0:
                pass
            else:
                self.rect.y -= self.v
            if self.k < 90:
                self.k += 1
        else:
            self.rect.y += self.v
            if self.k > -90:
                self.k -= 1
        if self.rect.y >= h - self.wi:
            runny = False
        if self.rect.x < (w - self.wi) // 3:
            self.rect.x += self.v
        if runny:
            self.map()
            self.time += 0.2
            if int(self.time) % 5 == 0:
                self.time = 1
            self.image = Bird.image.subsurface(int(self.time - 1) * Bird.qu, 0, 60, 60)
            self.image = pygame.transform.rotate(self.image, int(self.k))
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
            all_sprites.update()
            if score > record and rec:
                with open('best.txt', 'w') as file: file.write(str(int(score)))
                f2 = pygame.font.Font(None, 60)
                text2 = f2.render(f'Новый рекорд!', True, 'blue')
                screen.blit(text2, (w//2, h//2))
            f1 = pygame.font.Font(None, 100)
            text1 = f1.render(f'Счёт: {int(score)}', True,
                          'green')
            screen.blit(text1, (w//2, h//2 - 100))
        clock.tick(FPS)
        pygame.display.flip()