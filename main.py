import pygame
from win32api import GetSystemMetrics
from functools import cmp_to_key
from rect import TextBox
from keyboard import KeyboardKey


def compare(a, b):
    if a[0] < b[0] or (a[0] == b[0] and a[1] > b[1]):
        return -1
    if a[0] > b[0] or (a[0] == b[0] and a[1] < b[1]):
        return 1
    return 0


def scanline(a, x):
    """   scanline-algorithm

    :param a: ends of the segments
    :param x: question-points
    :return: answers for question-points"""
    s = [(a[i >> 1][i & 1], 1 - 2 * (i & 1), 0) for i in range(2 * len(a))] + [(x[i], 0, i) for i in range(len(x))]
    s.sort(key=cmp_to_key(compare))
    ans = [0 for _ in x]
    cur = 0
    for event in s:
        cur += event[1]
        if event[1] == 0:
            ans[event[2]] = cur
    return ans


def run():
    pygame.init()
    background_color = (255, 255, 255)
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    screen.fill(background_color)
    running = True
    segments = []
    points = []

    def enter_segment():
        nonlocal segments
        screen.fill(background_color)
        tb1 = TextBox('Введите начало:', (width // 5, height // 4), input_num=True)
        tb2 = TextBox('Введите конец:', tb1.bottom_pos(), input_num=True)
        segments.append((int(tb1.action()), int(tb2.action())))
        screen.fill(background_color)

    def enter_point():
        nonlocal points
        screen.fill(background_color)
        tb = TextBox('Введите точку:', (width // 5, height // 4), input_num=True)
        points.append(int(tb.action()))
        screen.fill(background_color)

    seg = int(TextBox('Кол-во отрезков:', (width // 5, height // 4), input_num=True).action())
    screen.fill(background_color)
    pt = int(TextBox('Кол-во точек:', (width // 5, height // 4), input_num=True).action())
    screen.fill(background_color)
    for _ in range(seg):
        enter_segment()
    for _ in range(pt):
        enter_point()
    tb_seg = TextBox(f'{segments}', (0, 0))
    tb_pt = TextBox(f'{points}', tb_seg.bottom_pos())
    tb_sl = TextBox(f'{scanline(segments, points)}', tb_pt.bottom_pos())
    tb_seg.blit()
    tb_pt.blit()
    tb_sl.blit()
    pygame.display.flip()
    pygame.time.wait(7000)


def main():
    pygame.init()
    screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), pygame.FULLSCREEN)

    running = True
    keyboard = dict((c, KeyboardKey()) for c in KeyboardKey.all_keys())
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.unicode in keyboard:
                keyboard[event.unicode].down()
            if event.type == pygame.KEYUP and event.unicode in keyboard:
                keyboard[event.unicode].up()
        tb0 = TextBox('Экран обновляется через 4 секунды после вывода суммы', (200, 200))
        tb1 = TextBox('Введите первое число:', tb0.bottom_pos(), input_num=True)
        tb2 = TextBox('Введите второе число:', tb1.bottom_pos(), input_num=True)
        tb1.action()
        if tb1.quit:
            break
        tb2.action()
        if tb2.quit:
            running = False
            continue
        tb3 = TextBox(f'Сумма чисел: {int(tb1.get_input()) + int(str(tb2.get_input()))}', tb2.bottom_pos(),
                      input_str=True)
        tb3.blit()
        pygame.display.flip()
        pygame.time.wait(4000)


if __name__ == '__main__':
    run()
