# coding: utf8
from jnp3.misc import deprecated


@deprecated("Use `math.gcd`")
def gcd(m, n):
    """返回两个数的最大公约数"""
    while m % n != 0:
        m, n = n, m % n
    return n


@deprecated("Use `pow`")
def power_(x, y, z):
    """x ** y % z"""
    if y == 1:
        return x % z
    else:
        if y % 2 == 0:
            half_y = y // 2
            return (power_(x, half_y, z) ** 2) % z
        else:
            half_y = (y - 1) // 2
            return (x * power_(x, half_y, z) ** 2) % z


def log_with_mim_base(power: int) -> tuple[int, int]:
    """将 n 拆解成 x**y 的形式

    三者都是正整数，
    其中 y 可以为 1，n 和 x 都不能为 1

    基本思路就是从 2~n 中一个个测试，
    找到一个能整除的数后就循环整除看看最后能不能除尽，
    如果能，那么循环的次数就是指数，如果不能，再尝试下一个

    :return 可拆解则返回 (x, y)，否则返回 (n, 1)
    """
    if power <= 2:
        return power, 1
    end = power
    for i in range(2, power):
        if i >= end:
            return power, 1
        end, rm = divmod(power, i)
        if rm == 0:
            y = 1
            e = end
            while e != 1:
                e, r = divmod(e, i)
                if r != 0:
                    break  # 当前值没有拆成功，继续尝试下一个值
                y += 1
            else:
                return i, y
    else:
        return power, 1  # 貌似只有 3 会走到这儿


def get_base(n: int, m: int) -> int | None:
    """如果 n = x**m 则返回 x，否则返回 None

    我们期望三者都是正整数
    """
    if n < 0 or m <= 0:
        return None
    if n == 0:
        return 0
    if n == 1 or m == 1:
        return 1
    x, y = log_with_mim_base(n)
    if y == 1:
        return None
    if m == y:
        return x
    else:
        dm = divmod(y, m)
        if dm[1] == 0:
            return pow(x, dm[0])
        else:
            return None


def get_base_with_coefficient(n: int, m: int) -> tuple[int, int] | None:
    """n = b * a ** m

    若 b 不包含能被 m 开方的因数，则返回 (a, b)，否则返回 None

    我们期望四者都是正整数，且 a > 1 且 m > 1
    """
    if n <= 1 or m <= 1:
        return None
    if n == 2 or n == 3:
        return None
    pos_a = get_base(n, m)
    if pos_a is not None:
        return pos_a, 1
    end = n
    for b in range(2, n):
        if b >= end:
            return None  # 理论上循环总会在这里结束
        end, r = divmod(n, b)
        if r == 0:
            # (a, b) 是唯一的吗？
            pos_a = get_base(end, m)
            if pos_a is not None:
                return pos_a, b
            ano_a = get_base(b, m)
            if ano_a is not None:
                return ano_a, end


if __name__ == '__main__':
    # import math
    # print(math.gcd(2160, 15360))
    # print(gcd(2160, 15360))

    print(get_base(65536, 16))
    print(get_base_with_coefficient(131072, 16))
