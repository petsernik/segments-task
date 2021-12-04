import pygame
from keyboard import Keyboard


class Rect:
    def __init__(self, rect=None):
        if rect is None:
            rect = [0, 0, 0, 0]
        self.rect = rect

    def width(self):
        return self.rect[2]

    def height(self):
        return self.rect[3]

    def pos(self):
        return self.rect[0], self.rect[1]

    def size(self):
        return self.rect[2], self.rect[3]

    def get_size(self):
        return self.rect[2], self.rect[3]

    def get_rect(self):
        return self.rect

    def upd_pos(self, x, y=None):
        if y is None:
            self.rect = [x[0], x[1], self.rect[2], self.rect[3]]
        else:
            self.rect = [x, y, self.rect[2], self.rect[3]]

    def upd_rect(self, x, y, w, h):
        self.rect = [x, y, w, h]

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

    def blit(self):
        if not self.hidden:
            pygame.display.get_surface().blit(self.image, self.rect)

    def action(self, as_btn=True):
        if (self.active and not self.hidden) or not as_btn:
            self.__action()
        self.active = False


class Text(Rect):
    def __init__(self, render_text):
        super().__init__()
        self.text = render_text
        self.rect = list(render_text.get_rect())

    def blit(self):
        pygame.display.get_surface().blit(self.text, self.rect)


class TextButton(Rect):
    def __init__(self, render_text):
        super().__init__()
        self.text = render_text
        self.res = ''
        self.rect = list(render_text.get_rect())
        self.hidden = False
        self.active = False
        self.__action = lambda: None

    def blit(self):
        if not self.hidden:
            pygame.display.get_surface().blit(self.text, self.rect)


class TextBox(Rect):
    def __init__(self, render_text, pos, input_box=None):
        super().__init__()
        rt = render_text
        if isinstance(rt, str):
            rt = pygame.font.Font(None, 48).render(rt, True, 'black')
        self.text = rt
        self.rect = list(rt.get_rect())
        self.upd_pos(pos)
        self.input_box = input_box
        if self.input_box is not None:
            x, y, w, h = self.rect
            self.input_box.upd_rect(x, y + h, w, h)
            self.input_box.parent = self

    def blit(self):
        pygame.display.get_surface().blit(self.text, self.rect)

    def action(self):
        if self.input_box is not None:
            self.input_box.action()


class InputBox(Rect):
    def __init__(self, pos=(0, 0), size=(0, 0),
                 allow_keys='qwertyuiopasdfghjklzxcvbnmёйцукенгшщзхъфывапролджэячсмитьбю'
                            'QWERTYUIOPASDFGHJKLZXCVBNMЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
                            '1234567890'
                            '+-*/='
                            '<>'
                            '~`!@#$%^&|\\/,. ', parent=None):
        super().__init__((pos[0], pos[1], size[0], size[1]))
        self.allow_keys = set(allow_keys)
        self.text = ''
        self.max_len = 1000000
        self.parent = parent

    def blit(self, color=(9, 255, 255)):
        screen = pygame.display.get_surface()
        x0, y0 = self.pos()
        x1, y1 = x0 + self.size()[0] - 1, y0 + self.size()[1] - 1
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.aalines(screen, 'black', True, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

    def add_key(self, key):
        if self.can_add():
            self.text += key

    def can_add(self):
        return len(self.text) < self.max_len

    def lc_motion(self, event):
        self.init()
        self.parent.rect[0] += event.rel[0]
        self.parent.rect[1] += event.rel[1]
        self.rect[0] += event.rel[0]
        self.rect[1] += event.rel[1]
        self.parent.blit()
        self.blit()

    def init(self):
        x, y, z, t = self.parent.rect
        _, _, dz, dt = self.rect
        z += dz
        t += dt
        pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), (x, y, z, t))

    def action(self, change=False, font=None, event_func=None, using_lc_motion=False):
        if not change:
            self.text = ''
        if font is None:
            font = pygame.font.Font(None, 48)

        running = True
        keyboard = Keyboard.keys
        mouse = {'lc': False, 'rc': False}

        while running:
            self.init()
            self.parent.blit()
            self.blit()
            for event in pygame.event.get():
                if event_func is not None:
                    event_func(self, event)
                Keyboard.update_key(event)
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.text = ''
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.unicode in self.allow_keys:
                        self.add_key(event.unicode)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse['lc'] = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse['lc'] = False
                if using_lc_motion and mouse['lc'] and event.type == pygame.MOUSEMOTION and \
                        (self.parent is not None and self.parent.collide_point(event.pos[0], event.pos[1]) or
                         self.collide_point(event.pos[0], event.pos[1])):
                    self.lc_motion(event)

            for k in keyboard:
                if k in self.allow_keys and keyboard[k].get_tick():  # stupid err: don't use tick by not allowed
                    self.add_key(k)
            if keyboard['space'].get_tick():
                self.text += ' '
            if keyboard['backspace'].get_tick(0.03):
                self.text = self.text[:-1]
            blit_text(pygame.display.get_surface(), self.text, self.pos(), font, allow_exceeding=True)
            pygame.display.flip()


class InputNumBox(InputBox):
    def __init__(self):
        super(InputNumBox, self).__init__(allow_keys='0123456789')
        self.max_len = 7

    @staticmethod
    def mul_by_minus(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
            if len(self.text) > 0:
                if self.text[0] == '-':
                    self.text = self.text[1:]
                else:
                    self.text = '-' + self.text

    def action(self, change=False, font=None, event_func=None, using_lc_motion=False):
        if event_func is None:
            super(InputNumBox, self).action(change, font, InputNumBox.mul_by_minus, using_lc_motion)
        else:
            super(InputNumBox, self).action(change, font, event_func, using_lc_motion)

    def can_add(self):
        return len(self.text) < self.max_len + self.text.startswith('-')


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
