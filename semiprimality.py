# -*- coding: utf-8 -*-

import math
import random
from itertools import islice, cycle, count, compress

N = 100000


def croft():  # наверняка поест память на больших числах
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
        return next(d) * next(d) == n
    except:
        return False


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


def is_prime(n):  # вероятностный алгоритм проверки на простость
    if n < 3:
        return True
    if n < 10:
        k = 2
    else:
        k = n/3 if n/3 < 20 else 20
    a_list = random.sample(range(1, n), k)
    for a in a_list:
        if (a**(n-1)) % n != 1:
            return False
    return True


def main():  # самая некрасивая функция из-за своих проверок
    discovered = False
    num = newton(N, f, f1, 1)  # нашли число, которое должно быть N-м по счёту. Ландау ручается, что так оно и есть :)
    num = int(math.floor(num))
    delta = 0
    while not discovered:
        if is_semiprime(num):
            discovered = True
        else:
            num = num + delta  # количество полупростых высчитывается не точно, соответсвуюющее число нужное число может оказаться в небольшом радиусе
            delta = -1*(abs(delta)+1)*(delta/abs(delta)) if delta else 1  # иногда нужно пометаться, если не натолкнулись на нужное число

    print num

if __name__ == '__main__':
    main()
