from functools import cmp_to_key


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
    print('Введите число отрезков:')
    n = int(input())
    print('Введите каждый отрезрок в виде пары чисел: начало, конец')
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
    print(a)


if __name__ == '__main__':
    run()
