import os, sys, random, pygame


pygame.init()
color = [0, 0, 0]
size = w, h = [1080, 720]
screen = pygame.display.set_mode(size)
xy = 20
n = 0
run = True


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
    image = load_image('img/'+ "tt.png")
    image = pygame.transform.scale(image, (100, 100))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bird.image
        self.rect = self.image.get_rect()
        self.wi, self.hi = self.image.get_size()
        self.rect.x = 0
        self.rect.y = 400
        self.k = 50
        self.choords = self.wi
        self.v = 5
        self.flag = 50


    def update(self, s=0):
        print(self.rect.x, self.rect.y, self.choords)
        if self.rect.y <= 0 and self.k < self.flag:
            self.k = self.flag
        elif self.rect.y >= h - self.wi:
            global run
            run = False
        elif s == 1 or self.k < 50:
            if s == 1:
                self.k = 0
            self.press()
        elif self.k < self.flag:
            self.k += 1
        elif self.rect.y < h and self.k == self.flag:
            self.rect.y += self.v
        if self.rect.x >= w:
            self.rect.x = 0 - self.wi
        if self.rect.x < (w - self.wi) // 4:
            self.rect.x += self.v
        self.map()

    def press(self):
        if self.rect.y != 0 and self.rect.y != h:
            self.rect.y -= self.v
        self.k += 1

    def map(self):
        self.choords += 1
        # if self.choords % 250 == 0:
        #     pass
        # self.v += 1
        # self.flag -= 1

    # def vel(self):
    #    global n
    #    if self.choords % 10 == 0:
    #        n += 1


if __name__ == "__main__":
    Bird(all_sprites)

    while run:
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    all_sprites.update(1)
        background_image = pygame.image.load('img/bg.png')
        background_image = pygame.transform.scale(background_image, size)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.time.delay(xy)
        pygame.display.flip()