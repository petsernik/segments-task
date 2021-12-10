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

        def clear():
            screen.fill(background_color)

        def draw_center_str(s, pos, color='black', font_size=30):
            s = str(s)
            TextBox(
                s,
                (pos[0], pos[1]),
                font_size=font_size,
                centering=True
            ).blit(color=color)

        pos = (10, 10)
        tb = TextBox('Покрасим концы каждого отрезка: начало синим цветом, конец красным.', pos)
        tb.blit()
        s = []
        draw_line()
        pause()
        val_dict = dict()
        pos_dict = dict()
        for i in range(2 * len(a)):
            v = (a[i >> 1][i & 1], 1 - 2 * (i & 1), 0)
            s.append(v)
            color = 'blue' if v[1] == 1 else 'red'
            p = (v[0] * 70 + width // 2, height // 2 - 25)
            if p not in val_dict:
                draw_center_str(v[0], p)
                val_dict[p] = v[0]
            p = (v[0] * 70 + width // 2, height // 2 + 5)
            while p in pos_dict:
                p = (p[0], p[1] + 30)
            draw_center_str(len(s), p, color)
            pos_dict[p] = True
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
            p = (v[0] * 70 + width // 2, height // 2 - 25)
            if p not in val_dict:
                draw_center_str(v[0], p)
                val_dict[p] = v[0]
            p = (v[0] * 70 + width // 2, height // 2 + 5)
            while p in pos_dict:
                p = (p[0], p[1] + 30)
            draw_center_str(len(s), p, color)
            pos_dict[p] = True
            pygame.draw.circle(screen, color, (v[0] * 70 + width // 2, height // 2), 5)
            pause()
        tb.clear()
        tb = TextBox('Отсортируем полученные точки по правилу: точка раньше в списке, '
                     'если её позиция меньше, а при равенстве позиций: если её цвет меньше (синий<желтый<красный).',
                     pos)
        tb.blit()
        pause()
        clear()
        tb = TextBox('Отсортировали! Это делается за O((n+q)log(n+q)).', pos)
        tb.blit()
        s.sort(key=cmp_to_key(compare))

        draw_line()
        for p, v in val_dict.items():
            draw_center_str(v, p)
        pos_dict.clear()
        for i in range(len(s)):
            v = s[i]
            color = ''
            if v[1] == -1:
                color = 'red'
            elif v[1] == 0:
                color = 'yellow'
            elif v[1] == 1:
                color = 'blue'
            pygame.draw.circle(screen, color, (v[0] * 70 + width // 2, height // 2), 5)
            p = (v[0] * 70 + width // 2, height // 2 + 5)
            while p in pos_dict:
                p = (p[0], p[1] + 30)
            pos_dict[p] = True
            draw_center_str(i + 1, p, color)
        pause()
        tb.clear()
        _x = -2 ** 32
        ans = [-1 for _ in x]
        cur = 0
        tb = TextBox('Теперь мы применим следующее соображение: количество отрезков, которым '
                     'может принадлежать точка x, меняется только когда x проходит через начало/конец одного '
                     f'из отрезков. Так давайте добавлять +1, когда '
                     f'проходим через синюю точку, и -1, когда через красную, '
                     f'когда мы проходим желтую точку (+0) выписываем для неё ответ: сумму всех +1 и -1 до'
                     f'неё (на каждом шаге мы помним сумму).\n'
                     f'Положим x={_x}, тогда сумма={cur}.', pos)
        tb1 = TextBox('Входные точки: ' + str(x) + '\nТекущий ответ: ' + str(ans),
                      tb.bottom_pos())
        tb.blit()
        tb1.blit()
        pause()
        pos_list = list(pos_dict.keys())
        for i in range(len(s)):
            v = s[i]
            color = ''
            if v[1] == -1:
                color = 'red'
            elif v[1] == 0:
                color = 'yellow'
            elif v[1] == 1:
                color = 'blue'
            pygame.draw.circle(screen, color, (v[0] * 70 + width // 2, height // 2), 5)
            event = s[i]
            tb.clear()
            _x = event[0]
            cur += event[1]
            if event[1] == 0:
                ans[event[2]] = cur
            tb = TextBox('Теперь мы применим следующее соображение: количество отрезков, которым '
                         'может принадлежать точка x, меняется только когда x проходит через начало/конец одного '
                         f'из отрезков. Так давайте добавлять +1, когда '
                         f'проходим через синюю точку, и -1, когда через красную, '
                         f'когда мы проходим желтую точку (+0) выписываем для неё ответ: сумму всех +1 и -1 до'
                         f'неё (на каждом шаге мы помним сумму).\n'
                         f'Положим x={_x}, тогда сумма={cur}.', pos)
            tb.blit()
            v = pos_list[i]
            pygame.draw.circle(screen, 'black', (v[0] - 15, v[1] + 10), 5)
            tb1.clear()
            tb1 = TextBox('Входные точки: ' + str(x) + '\nТекущий ответ: ' + str(ans),
                          tb.bottom_pos())
            tb1.blit()
            pause()
            pygame.draw.circle(screen, 'white', (v[0] - 15, v[1] + 10), 5)
        return ans

    pygame.init()
    background_color = (255, 255, 255)
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    screen.fill(background_color)
    segments = []
    points = []
    main_pos = (width // 5, height // 4)

    def enter_segment():
        nonlocal segments
        tb1 = TextBox('Введите начало отрезка:', main_pos, input_num=True)
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
        tb = TextBox('Введите точку:', main_pos, input_num=True)
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
                          (0, height // 4))
            tb2 = TextBox('Используйте клавишу ENTER, чтобы переходить на следующий слайд.\n'
                          'ESC, чтобы выйти из приложения.', tb1.bottom_pos())
            tb1.blit()
            tb2.blit()
            pygame.display.flip()
        elif run_screen == 1:
            screen.fill(background_color)
            segments.clear()
            points.clear()
            seg = read_positive(TextBox('Введите количество отрезков:', main_pos, input_num=True))
            screen.fill(background_color)
            for _ in range(seg):
                tb = TextBox(f'{_ + 1}/{seg}', (0, 0))
                tb.blit()
                enter_segment()
                tb.clear()
            pt = read_positive(TextBox('Введите количество точек:', main_pos, input_num=True))
            screen.fill(background_color)
            for _ in range(pt):
                tb = TextBox(f'{_ + 1}/{pt}', (0, 0))
                tb.blit()
                enter_point()
                tb.clear()
            visual_scanline(segments, points)
            TextBox('Алгоритм завершён! Нажмите ENTER, чтобы ввести новые данные.\n'
                    'ESC, чтобы выйти из приложения.', (10, height - 100)).blit()
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
