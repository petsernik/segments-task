from time import time
import pygame


class KeyboardKey:
    def __init__(self):
        self.is_pressed = False
        self.tick_seconds = self.seconds = time()
        self.tick = self.hold = False
        self.game_pause = True

    def down(self):
        self.is_pressed = True
        self.tick_seconds = self.seconds = time()
        self.tick = self.hold = False

    def up(self):
        self.is_pressed = False
        self.tick = self.hold = False

    def get_hold(self, _time=0.2):
        if self.is_pressed:
            if not self.hold:
                self.hold = time() - self.seconds >= _time
            return self.hold

    def get_tick(self, _time=0.2):
        if self.is_pressed and self.get_hold(0.6):
            if self.tick:
                self.tick_seconds = time()
                self.tick = False
                return True
            else:
                self.tick = time() - self.tick_seconds >= _time
                return False

    @staticmethod
    def all_keys():
        lst = []
        lst.extend(list('0123456789qwertyuiopasdfghjklzxcvbnm'))
        lst.extend([f'F{i}' for i in range(1, 13)])
        lst.extend(['ctrl', 'esc', 'space', 'left', 'right', 'up', 'down', 'backspace'])
        return lst


class Keyboard:
    keys = dict((key, KeyboardKey()) for key in KeyboardKey.all_keys())

    @staticmethod
    def update_key(event):
        if event.type == pygame.KEYDOWN:
            key = get_keyboard_key(event)
            if key in Keyboard.keys:
                Keyboard.keys[key].down()
        if event.type == pygame.KEYUP:
            key = get_keyboard_key(event)
            if key in Keyboard.keys:
                Keyboard.keys[key].up()


def update_key(event, keyboard):
    if event.type == pygame.KEYDOWN:
        key = get_keyboard_key(event)
        if key in keyboard:
            keyboard[key].down()
    if event.type == pygame.KEYUP:
        key = get_keyboard_key(event)
        if key in keyboard:
            keyboard[key].up()


def get_keyboard_key(event):
    if event.unicode in KeyboardKey.all_keys():
        return event.unicode
    if event.key == pygame.K_F1:
        return 'F1'
    if event.key == pygame.K_F2:
        return 'F2'
    if event.key == pygame.K_F3:
        return 'F3'
    if event.key == pygame.K_F4:
        return 'F4'
    if event.key == pygame.K_F5:
        return 'F5'
    if event.key == pygame.K_F6:
        return 'F6'
    if event.key == pygame.K_F7:
        return 'F7'
    if event.key == pygame.K_F8:
        return 'F8'
    if event.key == pygame.K_F9:
        return 'F9'
    if event.key == pygame.K_F10:
        return 'F10'
    if event.key == pygame.K_F11:
        return 'F11'
    if event.key == pygame.K_F12:
        return 'F12'
    if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
        return 'ctrl'
    if event.key == pygame.K_ESCAPE:
        return 'esc'
    if event.key == pygame.K_SPACE:
        return 'space'
    if event.key == pygame.K_LEFT:
        return 'left'
    if event.key == pygame.K_RIGHT:
        return 'right'
    if event.key == pygame.K_UP:
        return 'up'
    if event.key == pygame.K_DOWN:
        return 'down'
    if event.key == pygame.K_BACKSPACE:
        return 'backspace'
    return 'None'
