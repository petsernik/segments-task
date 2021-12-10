import pygame
import sys
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

    def move(self, x, y=None):
        if y is None:
            self.rect[0] += x[0]
            self.rect[1] += x[1]
        else:
            self.rect[0] += x
            self.rect[1] += y

    def top_pos(self):
        return self.rect[0], self.rect[1] - self.rect[3] - 20

    def bottom_pos(self):
        return self.rect[0], self.rect[1] + self.rect[3] + 20

    def offset(self, x, y):
        return [self.x() - x, self.y() - y]

    def offset_x(self, x):
        return self.x() - x

    def offset_y(self, y):
        return self.y() - y

    def x(self):
        return self.rect[0]

    def y(self):
        return self.rect[1]

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
    def __init__(self, text, pos, input_str=False, input_num=False):
        super().__init__()
        self.text = text
        self.upd_pos(pos)
        self.rect = get_rect_blit_text(pygame.display.get_surface(), self.text, self.pos(), pygame.font.Font(None, 48))
        self.input_box = InputBox()
        if input_str:
            self.create_input()
        elif input_num:
            self.create_input_num()
        self.quit = False
        self.have_input = input_str or input_num

    def blit(self, time=None):
        pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), self.rect)
        blit_text(pygame.display.get_surface(), self.text, self.pos(), pygame.font.Font(None, 48))
        if time is not None:
            pygame.display.flip()
            pygame.time.wait(time)
            self.clear()

    def clear(self):
        pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), self.rect)

    def action(self):
        if self.have_input:
            self.input_box.action()
            return self.input_box.text

    def input_init(self):
        x, y, w, h = self.rect
        inbox = self.input_box
        inbox.upd_pos(x + w + 10, y)
        iw, ih = inbox.size()
        self.upd_rect(x, y, inbox.offset_x(x) + iw, inbox.offset_y(y) + ih)
        inbox.parent = self
        self.have_input = True

    def create_input(self):
        x, y, w, h = self.rect
        self.input_box = InputBox(size=(w, h))
        self.input_init()

    def create_input_num(self):
        x, y, w, h = self.rect
        self.input_box = InputNumBox(size=(w, h))
        self.input_init()

    def get_input(self):
        return self.input_box.text


class InputBox(Rect):
    def __init__(self, pos=(0, 0), size=(0, 0),
                 allow_keys='qwertyuiopasdfghjklzxcvbnmёйцукенгшщзхъфывапролджэячсмитьбю'
                            'QWERTYUIOPASDFGHJKLZXCVBNMЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
                            '1234567890'
                            '+-*/='
                            '<>'
                            '~`!?\':;[]{}\"@#$%^&|\\/,. ', parent=None):
        super().__init__([pos[0], pos[1], size[0], size[1]])
        self.allow_keys = set(allow_keys)
        self.text = ''
        self.max_len = 1000000
        self.parent = parent
        self.font = pygame.font.Font(None, 48)

    def blit(self, color_rect=(9, 255, 255)):
        screen = pygame.display.get_surface()
        x0, y0 = self.pos()
        x1, y1 = x0 + self.size()[0] - 1, y0 + self.size()[1] - 1
        pygame.draw.rect(screen, color_rect, self.rect)
        pygame.draw.aalines(screen, 'black', True, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)])

    def add_key(self, key):
        if self.can_add():
            self.text += key

    def can_add(self):
        return len(self.text) < self.max_len

    def lc_motion(self, event):
        self.init()
        self.parent.move(event.rel)
        self.move(event.rel)
        self.parent.blit()
        self.blit()

    def init(self):
        self.parent.clear()

    def action(self, change=False, font=None, event_func=None, using_lc_motion=False):
        if not change:
            self.text = ''
        if font is None:
            font = self.font

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
                    self.parent.quit = True
                    sys.exit()
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
            blit_text(pygame.display.get_surface(), self.text, self.pos(), font, rect=self.rect)
            pygame.display.flip()


class InputNumBox(InputBox):
    def __init__(self, pos=(0, 0), size=(0, 0), allow_keys='0123456789', parent=None):
        super(InputNumBox, self).__init__(pos, size, allow_keys, parent)
        self.max_len = 1
        self.rect[2] = (self.max_len + 2) * self.font.size('0')[0]

    @staticmethod
    def mul_by_minus(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
            if self.text.startswith('-'):
                self.text = self.text[1:]
            else:
                self.text = '-' + self.text

    def action(self, change=False, font=None, event_func=None, using_lc_motion=False):
        if event_func is None:
            super(InputNumBox, self).action(change, font, InputNumBox.mul_by_minus, using_lc_motion)
        else:
            super(InputNumBox, self).action(change, font, event_func, using_lc_motion)
        try:
            int(self.text)
        except ValueError:
            self.text = '0'
            self.blit()
            blit_text(pygame.display.get_surface(), self.text, self.pos(), self.font, rect=self.rect)
            if not self.parent.quit:
                pygame.display.flip()

    def can_add(self):
        return len(self.text) < self.max_len + self.text.startswith('-')


def blit_text(surface, text, _pos, font, color='black', allow_exceeding=True, with_blit=True, rect=None):
    lines = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    pos = _pos
    x0, y0, width, height = surface.get_rect()
    if rect is not None:
        x0, y0, width, height = rect
        pos = [0, 0]
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


def get_rect_blit_text(surface, text, _pos, font, color='black', allow_exceeding=True, with_blit=False, rect=None):
    lines = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    pos = _pos
    x0, y0, width, height = surface.get_rect()
    if rect is not None:
        x0, y0, width, height = rect
        pos = [0, 0]
    max_x, max_y = x0 + width, y0 + height
    x, y = x0 + pos[0], y0 + pos[1]
    res_x = _pos[0]
    res_y = _pos[1]
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
            res_x = max(x + word_width, res_x)
            res_y = max(y + word_height, res_y)
            x += word_width + space
        x = x0 + pos[0]  # Reset the x.
        y += word_height  # Start on new row.
    return x0 + pos[0], y0 + pos[1], res_x - (x0 + pos[0]), res_y - (y0 + pos[1])
