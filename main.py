import pygame
import sys
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
    def event_handler():
        nonlocal run_screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if run_screen == 0 or run_screen == 2:
                    run_screen = 1
                elif run_screen == 1:
                    return True
        return False

    def visual_scanline(a, x):
        """   scanline-algorithm

        :param a: ends of the segments
        :param x: question-points
        :return: answers for question-points"""

        def pause(condition=True):
            pygame.display.flip()
            while condition and not event_handler():
                pass

        def draw_line():
            pygame.draw.aalines(screen, 'black', True, [(0, height // 2), (width, height // 2)])

        pos = (10, 10)
        tb = TextBox('Покрасим концы каждого отрезка: начало синим цветом, конец красным.', pos)
        tb.blit()
        s = []
        draw_line()
        pause()
        for i in range(2 * len(a)):
            v = (a[i >> 1][i & 1], 1 - 2 * (i & 1), 0)
            s.append(v)
            color = 'blue' if v[1] == 1 else 'red'
            TextBox(
                f'{v[0]}',
                (v[0] * 70 + width // 2, height // 2 - 25),
                font_size=30,
                centering=True
            ).blit()
            pygame.draw.circle(screen, color, (v[0] * 70 + width // 2, height // 2), 5)
            pygame.display.flip()
            pause(v[1] == -1)
        tb.clear()
        tb = TextBox('Точки, для которых нужно выводить ответ, покрасим жёлтым.', pos)
        tb.blit()
        pause()
        for i in range(len(x)):
            v = (x[i], 0, i)
            s.append(v)
            color = 'yellow'
            TextBox(
                f'{v[0]}',
                (v[0] * 70 + width // 2, height // 2 - 25),
                font_size=30,
                centering=True
            ).blit()
            pygame.draw.circle(screen, color, (v[0] * 70 + width // 2, height // 2), 5)
            pause()
        tb.clear()

        s.sort(key=cmp_to_key(compare))
        ans = [0 for _ in x]
        cur = 0
        for event in s:
            cur += event[1]
            if event[1] == 0:
                ans[event[2]] = cur
        return ans

    pygame.init()
    background_color = (255, 255, 255)
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    screen.fill(background_color)
    segments = []
    points = []
    pos = (width // 5, height // 4)

    def enter_segment():
        nonlocal segments
        screen.fill(background_color)
        tb1 = TextBox('Введите начало отрезка:', pos, input_num=True)
        tb2 = TextBox('Введите конец отрезка:', tb1.bottom_pos(), input_num=True)
        tb1.blit()
        tb2.blit()
        a, b = int(tb1.action()), int(tb2.action())
        while a > b:
            tb1.clear()
            tb2.clear()
            tb1.blit()
            tb2.blit()
            TextBox('Второе число должно быть не меньше первого!', tb1.top_pos()).blit()
            a, b = int(tb1.action()), int(tb2.action())
        segments.append((a, b))
        screen.fill(background_color)

    def enter_point():
        nonlocal points
        screen.fill(background_color)
        tb = TextBox('Введите точку:', pos, input_num=True)
        points.append(int(tb.action()))
        screen.fill(background_color)

    def read_positive(tb):
        a = int(tb.action())
        while a <= 0 and not tb.quit:
            TextBox('Число должно быть положительным!', tb.top_pos()).blit()
            a = int(tb.action())
        screen.fill(background_color)
        return a

    run_screen = 0
    while True:
        event_handler()
        if run_screen == 0:
            screen.fill(background_color)
            tb1 = TextBox('Данное приложение визуалирует работу метода \" сканирующая прямая\" '
                          'для решения задачи \"скольким отрезкам принадлежит данная точка\" '
                          'с асимптотикой O((n+q)log(n+q)), '
                          'где n - количество отрезков, q - количество точек.',
                          (0, height // 7))
            tb2 = TextBox('Нажимайте клавишу ENTER, чтобы переходить на следующий слайд.\n'
                          'ESC, чтобы выйти из приложения.', tb1.bottom_pos())
            tb1.blit()
            tb2.blit()
            pygame.display.flip()
        elif run_screen == 1:
            screen.fill(background_color)
            seg = read_positive(TextBox('Введите количество отрезков:', pos, input_num=True))
            pt = read_positive(TextBox('Введите количество точек:', pos, input_num=True))

            for _ in range(seg):
                enter_segment()

            for _ in range(pt):
                enter_point()

            visual_scanline(segments, points)
            TextBox('Алгоритм завершён! Нажмите ENTER, чтобы начать сначала.', (10, height - 50)).blit()
            pygame.display.flip()
            run_screen = 2
        elif run_screen == 2:
            pass


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
