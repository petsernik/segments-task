import pygame
from win32api import GetSystemMetrics
from functools import cmp_to_key
from rect import InputBox, InputNumBox, TextBox
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
    s = a + [(x[i], 0, i) for i in range(len(x))]
    s.sort(key=cmp_to_key(compare))
    ans = [0 for _ in x]
    cur = 0
    for event in s:
        cur += event[1]
        if event[1] == 0:
            ans[event[2]] = cur
    return ans


def run():
    # print('Введите число отрезков:')
    # n = int(input())
    # print('Введите каждый отрезок в виде пары чисел: начало, конец')
    # a = list([0 for _ in range(2 * n)])
    # for j in range(n):
    #     s = list(map(int, input().split()))
    #     a[2 * j] = (s[0], 1)
    #     a[2 * j + 1] = (s[1], -1)
    # print('Введите число точек:')
    # n = int(input())
    # print('Введите точки (по одному числу):')
    # x = [int(input()) for _ in range(n)]
    # print(f'Ответ: ')
    # for ans in scanline(a, x):
    #     print(ans, end=' ')

    pygame.init()
    screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), pygame.FULLSCREEN)
    running = True
    segments = []

    def enter_seg():
        nonlocal segments
        screen.fill((255, 255, 255))
        tb1 = TextBox('Введите первое число:', (GetSystemMetrics(0) // 5, GetSystemMetrics(1) // 4), input_num=True)
        tb2 = TextBox('Введите второе число:', tb1.bottom_pos(), input_num=True)
        tb1.action()
        if tb1.quit:
            TextBox('Отменено!', tb2.bottom_pos()).blit()
            pygame.display.flip()
            pygame.time.wait(1000)
            return True
        tb2.action()
        if tb2.quit:
            TextBox('Отменено!', tb2.bottom_pos()).blit()
            pygame.display.flip()
            pygame.time.wait(1000)
            return True
        segments.append((int(tb1.get_input()), int(tb2.get_input())))
        TextBox('Успешно!', tb2.bottom_pos()).blit()
        pygame.display.flip()
        screen.fill((255, 255, 255))
        pygame.time.wait(1000)

    enter_seg()
    enter_seg()
    TextBox(f'до сортировки: {str(segments)}', (0, 0)).blit(2000)
    segments.sort()
    TextBox(f'после сортировки: {str(segments)}', (0, 0)).blit(2000)


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
