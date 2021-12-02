import pygame
from keyboard import Keyboard


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
    def __init__(self, render_text):
        super().__init__()
        self.text = render_text
        self.res = ''
        self.rect = list(render_text.get_rect())
        self.hidden = False
        self.active = False
        self.__action = lambda: None


class TextBox(Rect):
    def __init__(self, render_text):
        super().__init__()
        self.text = render_text
        self.rect = list(render_text.get_rect())
        self.hidden = False
        self.active = False
        self.__action = lambda: None


class InputBox(Rect):
    def __init__(self, pos=(10, 10), size=(200, 200)):
        super().__init__((pos[0], pos[1], size[0], size[1]))
        s = '01234567890qwertyuiopasdfghjklzxcvbnmёйцукенгшщзхъфывапролджэячсмитьбю '
        self.allow_keys = set(s)
        self.allow_keys |= set(s.upper())
        self.active = False
        self.text = ''

    @staticmethod
    def blit(s, pos, area=None):
        if area is None:
            pygame.display.get_surface().blit(s, pos)
        else:
            pygame.display.get_surface().blit(s, pos, area)

    def action(self, font=None):
        keyboard = Keyboard.keys
        if font is None:
            font = pygame.font.Font(None, 48)
        screen = pygame.display.get_surface()
        x0, y0 = self.pos()
        x1, y1 = x0 + self.size()[0], y0 + self.size()[1]
        while self.active:
            screen.fill((9, 255, 255), self.rect)
            pygame.draw.aalines(screen, 'black', True, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
            for event in pygame.event.get():
                Keyboard.update_key(event)
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.text = ''
                    self.active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.unicode in self.allow_keys:
                        self.text += event.unicode
            for k in keyboard:
                if k in self.allow_keys and keyboard[k].get_tick():  # stupid err: don't use tick by not allowed
                    self.text += k
            if keyboard['space'].get_tick():
                self.text += ' '
            if keyboard['backspace'].get_tick(0.03):
                self.text = self.text[:-1]
            blit_text(self, self.text, (0, 0), font, allow_exceeding=True)
            pygame.display.flip()


def blit_text(surface, text, pos, font, color='black', allow_exceeding=True, with_blit=True):
    lines = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    x0, y0, width, height = surface.get_rect()
    max_x, max_y = x0 + width, y0 + height
    x, y = x0 + pos[0], y0 + pos[1]
    for line in lines:
        word_width, word_height = 0, 0
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_x and x != x0 + pos[0]:
                x = x0 + pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            if not allow_exceeding:
                if x + word_width > max_x or y + word_height > max_y:
                    raise Exception('Text is so long')
            if with_blit:
                surface.blit(word_surface, (x, y), (0, 0, max_x - x, max_y - y))
            x += word_width + space
        x = x0 + pos[0]  # Reset the x.
        y += word_height  # Start on new row.
