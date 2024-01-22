import os, sys, random, pygame

pygame.init()
color = [0,0,0]
size = w, h = [800, 800]
screen = pygame.display.set_mode(size)
xy = 20
n = 0


def load_image(name, colorkey=None):
    fullname = os.path.join("../img", name)
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


class Bomb(pygame.sprite.Sprite):
    image = load_image("pon.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.wi, self.hi = self.image.get_size()
        self.rect.x = 0
        self.rect.y = 400
        self.k = 50
        self.choords = self.wi
        self.v = 1
        self.flag = 65

    def update(self, s=0):
        print(h+self.hi)
        if self.rect.y == 0 or self.rect.y == h + self.hi:
            running = False
        elif s == 1 or self.k < 50:
            if s == 1:
                self.k = 0
            self.press()
        elif self.k < self.flag:
            self.k += 1
            self.rect.x += self.v
        elif self.rect.y < h and self.k == self.flag:
            self.rect.y += self.v
            self.rect.x += self.v
        if self.rect.x >= w:
            self.rect.x = 0 - self.wi
        self.map()

    def press(self):
        if self.rect.y != 0 and self.rect.y != h:
            self.rect.y -= 3
            self.rect.x += 1
        self.k += 1

    def map(self):
        self.choords += 1
        if self.choords % 250 == 0:
            #self.v += 1
            self.flag -= 1

    #def vel(self):
    #    global n
    #    if self.choords % 10 == 0:
    #        n += 1

Bomb(all_sprites)

running = True
while running:
    pygame.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                all_sprites.update(1)
    screen.fill(pygame.Color('white'))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.time.delay(xy - n)
    pygame.display.flip()

