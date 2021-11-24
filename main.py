# import pygame
from functools import cmp_to_key


# from win32api import GetSystemMetrics


# from rect import Button,
def compare(a, b):
    if a[0] < b[0]:
        return -1
    if a[0] > b[0]:
        return 1
    if a[1] > b[1]:
        return -1
    if a[1] < b[1]:
        return 1
    return 0


def scanline(a, x):
    a.extend([(x[i], 0, i) for i in range(len(x))])
    ans = [0 for _ in x]
    a.sort(key=cmp_to_key(compare))
    cur = 0
    for event in a:
        cur += event[1]
        if event[1] == 0:
            ans[event[2]] = cur
    return ans


def run():
    # pygame.init()
    # screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), pygame.FULLSCREEN)
    print('Введите число отрезков:')
    n = int(input())
    print('Введите каждую пару в виде пары чисел: начало, конец')
    a = list([0 for _ in range(2 * n)])
    for j in range(n):
        s = list(map(int, input().split()))
        a[2 * j] = (s[0], 1)
        a[2 * j + 1] = (s[1], -1)
    print('Введите число точек:')
    n = int(input())
    print('Введите точки (по одному числу):')
    x = [int(input()) for _ in range(n)]
    print(f'Ответ: ')
    for ans in scanline(a, x):
        print(ans, end=' ')


if __name__ == '__main__':
    run()
