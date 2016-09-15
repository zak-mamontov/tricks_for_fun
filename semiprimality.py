import math
import random

N = 1000


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
        a = 1  # a и b - множители бипростого числа
        b = 0
        num = num + delta if num + delta > 0 else 1  # количество полупростых высчитывается не точно, соответсвуюющее число нужное число может оказаться в небольшом радиусе
        delta = -1*(abs(delta)+1)*(delta/abs(delta)) if delta else 1  # иногда нужно пометаться, если не натолкнулись на нужное число
        while b < 2 and a <= num**0.5+1:
            a += 1
            while not is_prime(a):
                a += 1
            b = num/a if num % a == 0 and is_prime(num/a) else 0

        if a < num**0.5 + 1 and b != 0:
            discovered = True
    print num

if __name__ == '__main__':
    main()
