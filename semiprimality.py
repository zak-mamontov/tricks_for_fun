# -*- coding: utf-8 -*-
import sys
import math
import random
from itertools import islice, cycle, count, compress

N = int(sys.argv[1])


def croft():  # спираль Крофта
    for p in (2, 3, 5):
        yield p
    roots = {9: 3, 25: 5}
    primeroots = frozenset((1, 7, 11, 13, 17, 19, 23, 29))
    selectors = (1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0)
    for q in compress(
            islice(count(7), 0, None, 2),
            cycle(selectors)
    ):
        if q in roots:
            p = roots[q]
            del roots[q]
            x = q + 2*p
            while x in roots or (x % 30) not in primeroots:
                x += 2*p
            roots[x] = p
        else:
            roots[q*q] = q
            yield q
primes = croft


def decompose(n):  # собственно, бьём на множители
    for p in primes():
        if p*p > n:
            break
        while n % p == 0:
            yield p
            n //= p
    if n > 1:
        yield n


def is_semiprime(n):  # алгоритм проверки на полупростоту
    d = decompose(n)
    try:
        a, b = next(d), next(d)
        return a*b == n, a, b
    except:
        return False, 0, 0


def is_prime(n):  # алгоритм проверки на пустоту, использующий теперь спираль Крофта
    return list(zip((True, False), decompose(n)))[-1][0]


def f(x):  # функция по которой считается примерное количество полупростых на отрезке [0, x]
    return(math.log1p(x) - x**(float(N)/x))


def f1(x):  # производная от этой функции
    return(float(1)/x + N*(math.log1p(x)-1)*x**(N/x-2))


def newton(x0, f, f1, e):  # метод Ньютона численного решения уравнений. Им мы и найдём близкое к искомому число
    while True:
        x1 = x0 - (f(x0) / f1(x0))
        if abs(x1 - x0) < e:
            return x1
        x0 = x1


def main():  # самая некрасивая функция из-за своих проверок
    discovered = False
    num = newton(N, f, f1, 1)  # нашли число, которое должно быть N-м по счёту. Ландау ручается, что так оно и есть :)
    num = int(math.floor(num))
    delta = 0
    res = [False, ]
    while not discovered:
        res = is_semiprime(num)
        if res[0]:
            discovered = True
        else:
            num = num + delta  # количество полупростых высчитывается не точно, соответсвуюющее число нужное число может оказаться в небольшом радиусе
            delta = -1*(abs(delta)+1)*(delta/abs(delta)) if delta else 1  # иногда нужно пометаться, если не натолкнулись на нужное число

    print(num, res[1], res[2])

if __name__ == '__main__':
    main()
