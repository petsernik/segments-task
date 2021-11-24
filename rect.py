class Rect:
    def __init__(self, rect=(0, 0, 0, 0)):
        self.rect = rect

    def width(self):
        return self.rect[2]

    def height(self):
        return self.rect[3]

    def pos(self):
        return self.rect[0], self.rect[1]

    def size(self):
        return self.rect[2], self.rect[3]

    def upd_pos(self, x, y):
        self.rect[0], self.rect[1] = x, y

    def upd_rect(self, x, y, w, h):
        self.rect = (x, y, w, h)

    def collide_point(self, x, y):
        return self.rect[0] <= x <= self.rect[0] + self.rect[2] \
               and self.rect[1] <= y <= self.rect[1] + self.rect[3]


def fill(surface, color):
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            if surface.get_at((x, y))[3] > 0:
                surface.set_at((x, y), color)


class Button(Rect):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = list(image.get_rect())
        self.hidden = False
        self.active = False
        self.__action = lambda: None

    def set_color(self, color):
        self.image = self.image.convert_alpha()
        fill(self.image, color)

    def set_action(self, action):
        self.__action = action

    def collide_point(self, x, y):
        return not self.hidden and super().collide_point(x, y)

    def blit(self, screen):
        if not self.hidden:
            screen.blit(self.image, self.rect)

    def action(self, as_btn=True):
        if (self.active and not self.hidden) or not as_btn:
            self.__action()
        self.active = False


class Text(Rect):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.rect = list(text.get_rect())


class TextButton(Rect):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.res = ''
        self.rect = list(text.get_rect())
        self.hidden = False
        self.active = False
        self.__action = lambda: None


