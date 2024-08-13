# coding: utf8
from __future__ import annotations

import re as _re
from math import gcd as _gcd


class Decimal(object):
    """小数，辅助表示浮点数的类"""

    def __init__(self, decimal='0.0'):
        # 整数，和小数点偏移位数（右正，通常为负）
        self._int, self._fra = self._convert(decimal)

    @classmethod
    def _convert(cls, s_float):
        m = _re.match(r"^-?[0-9]+[.][0-9]+$", s_float)
        if m is None:
            raise ValueError("Invalid float format")
        s = m.group()
        # 取出符号
        sign, dec = (1, s) if s[0] != '-' else (-1, s[1:])
        # 去除收尾的0，
        # 注意，此时0.001变成了.001，
        # 12.0变成了12.，
        # 但它们都依然适应于后面的计算
        # 0.0变成了.，后面有单独处理
        dec = dec.strip('0')
        ln = len(dec)
        dot = dec.index('.')
        # 小数位数
        frc = ln - dot - 1
        # 整数部分
        dec = dec.replace('.', '')
        dec = '0' if len(dec) == 0 else dec
        ing = int(dec) * sign
        # 此时整数有可能形如234000，暂不处理这种，没看出必要性
        return ing, -frc

    @property
    def data(self):
        return self._int, self._fra

    def __repr__(self):
        return f"Decimal({self._int, self._fra})"

    def __str__(self):
        sign = '-' if self._int < 0 else ''
        if self._fra < 0:
            i = f"{abs(self._int):>0{abs(self._fra)}}"
            return sign + i[:self._fra] + '.' + i[self._fra:]
        else:
            i = f"{abs(self._int):<0{abs(self._fra)}}"
            return sign + i + '.0'

    def __eq__(self, other):
        """只实现了与 0 的比较"""
        if other == 0:
            return self._int == 0 and self._fra == 0
        else:
            # undefined
            raise NotImplementedError


class Rational(object):
    """有理数，即分数"""

    def __init__(self, top: PreciseNumbers, bottom: PreciseNumbers = 1):
        if bottom == 0:
            raise ZeroDivisionError("The denominator cannot be zero")
        self._num, self._den = self._reduce(top, bottom)

    @staticmethod
    def _signed_gcd(a: int, b: int) -> int:
        """
        跟 math.gcd(a, b) 一样，但符号与 b 的符号一致
        """
        g = _gcd(a, b)
        k = -1 if b < 0 else 1
        return k * g

    @staticmethod
    def _transect(val: PreciseNumbers, u: int, v: int) -> tuple[int, int]:
        """
        这个函数主要就是把 val * u/v，就是一个简单的乘法，
        然后把结果的分子分母单独返回，但是因为在 _reduce 时
        该对象本身都还没构建完成，所以无法用 __mul__ 去实现，
        所以只能是这里手动操作了
        """
        if isinstance(val, int):
            return val * u, v
        if isinstance(val, Rational):
            return val._num * u, val._den * v
        elif isinstance(val, Decimal):
            i, f = val.data
            if f > 0:
                return i * (10 ** f) * u, v
            else:
                return i * u, (10 ** -f) * v

        raise TypeError(f"Unsupported type {type(val).__name__}, for now")

    @classmethod
    def _reduce(cls, a: PreciseNumbers, b: PreciseNumbers) -> tuple[int, int]:
        """化简约分"""
        x, y = 1, 1
        x, y = cls._transect(a, x, y)
        y, x = cls._transect(b, y, x)  # b 是分母，要反着来
        g = cls._signed_gcd(x, y)
        return x // g, y // g

    def __repr__(self):
        return f"Rational({self._num}, {self._den})"

    def __str__(self):
        bot = f"/{self._den}" if self._den != 1 else ""
        return f"{self._num}{bot}"

    @property
    def data(self):
        return self._num, self._den

    @property
    def numerator(self):
        return self._num

    @property
    def denominator(self):
        return self._den

    def __eq__(self, other):
        other = Rational(other)
        return self.data == other.data

    def __add__(self, other):
        other = Rational(other)
        top = self._num * other._den + other._num * self._den
        bot = self._den * other._den
        return Rational(top, bot)

    def __sub__(self, other):
        other = Rational(other)
        top = self._num * other._den - other._num * self._den
        bot = self._den * other._den
        return Rational(top, bot)

    def __mul__(self, other):
        other = Rational(other)
        return Rational(self._num * other._num, self._den * other._den)

    def __truediv__(self, other):
        other = Rational(other)
        return Rational(self._num * other._den, self._den * other._num)

    def __neg__(self):
        return Rational(-1 * self._num, self._den)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -(self - other)

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        other = Rational(other)
        return Rational(self._den * other._num, self._num * other._den)


class RealFloat(object):
    """精确的浮点数

    RealFloat 通过整数加浮动小数点位数的方式表示浮点数，
    在运算处理上有优势，因此 RealFloat 对象自身支持运算

    使用说明：
        如果要处理的小数位数不会多于 15 位，这是 Python 的 float 类型可以处理的
        范围，建议直接用这个内置的 float，如果位数多于 15 位，又要求十分精确
        且涉及到运算，再考虑用此类。

        此类接受两个参数，第一个参数理论上可以是任何有符号数，但目前支持
            int, float, RealFloat
        类型，后续会添加其它类型。
        第二个参数是在第一个参数的小数点位置的基础上再偏移的位数，要求必须是整数
        （广义整数，并不一定是 int），若向左浮动，则为负，反之为正，零不浮动。

        类内会以最简形式维护浮点数的两个部分，举例：
        RealFloat(100, 0) 内部会保存为 (1, 2)；
        RealFloat(1.23, -2) 内部会保存为 (123, -4)；
        RealFloat(30.0, -1) 内部会保存为 (3, 0)；
        请_不要_改变这一规则。

    """

    def __init__(self, number, offset=0):
        try:
            offset = int(offset)  # 我们认为不能转成int的类型都不是整数
        except Exception:
            errmsg = '[ERROR] 偏移量必须可转换为整数'
            raise TypeError(errmsg)
        self.real_int, self.offset = self._simplify(number, offset)
        self._reserve = 20  # 小数保留位数，只在做除法时有用

    @property
    def reserve(self):
        return self._reserve

    @reserve.setter
    def reserve(self, value):
        if isinstance(value, int) and value >= 0:
            self._reserve = value
        else:
            errmsg = '[ERROR] 保留位数必须为整数且不能为负'
            raise ValueError(errmsg)

    @classmethod
    def _simplify(cls, number, offset):
        if number == 0:
            return 0, 0
        # 整数
        if isinstance(number, int):
            while str(number).endswith('0'):
                number //= 10
                offset += 1
            return number, offset
        # 浮点数
        if isinstance(number, float):
            dig, frc = str(number).split('.')
            while frc not in ('0', ''):
                dig += frc[0]
                frc = frc[1:]
                offset -= 1
            # 继续去整数那里判断零结尾，例：100.0
            return cls._simplify(int(dig), offset)

        # todo there are other more possibilities
        return number, offset

    def __repr__(self) -> str:
        if self.offset >= 0:
            return f"{self.real_int}{'0'*self.offset}.0"
        else:
            sign = '-' if self.real_int < 0 else ''
            after_offset = f"{abs(self.real_int):>0{-self.offset}}"
            f = after_offset[:self.offset]
            f = '0' if f == '' else f
            b = after_offset[self.offset:]
            b = ''.join(list(reversed(b)))
            b = str(int(b))  # 形如 b = '6500' or '000' => '56' or '0'
            b = ''.join(list(reversed(b)))  # '56' => '65', 总：'6500' => '65'
            return f"{sign}{f}.{b}"

    __str__ = __repr__

    def _convert(self, val):
        if isinstance(val, RealFloat):
            return val
        elif isinstance(val, (int, float)):
            num, oft = self._simplify(val, 0)
            return RealFloat(num, oft)
        else:
            raise TypeError("[ERROR] unsupported type for RealFloat")

    def __neg__(self):
        return RealFloat(-self.real_int, self.offset)

    def __add__(self, other):
        other = self._convert(other)
        if self.offset == other.offset:
            return RealFloat(self.real_int + other.real_int, self.offset)
        else:
            f_dic = {self.offset: self.real_int, other.offset: other.real_int}
            dif = abs(self.offset - other.offset)
            one_r = f_dic[max(self.offset, other.offset)] * (10 ** dif)
            min_oft = min(self.offset, other.offset)
            other_r = f_dic[min_oft]
            return RealFloat(one_r + other_r, min_oft)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        # 避免多次转换other
        return -(-self + other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = self._convert(other)
        return RealFloat(self.real_int * other.real_int, self.offset + other.offset)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        other = self._convert(other)
        oft = self._reserve + (self.offset - other.offset)  # 必须是被除数的offset减除数的
        if oft < 0:
            print("[WARNING] 保留位数太少，结果可能不准确")
        num = (self.real_int * 10**oft) // other.real_int
        return RealFloat(num, -self._reserve)

    def __rtruediv__(self, other):
        pass


PreciseNumbers = int | Rational | Decimal | RealFloat


if __name__ == '__main__':
    r = Rational(15360, 2160)
    print(repr(r))
    d = Decimal("1.234")
    print(repr(d))
    f = RealFloat(1.234, -20)
    print(repr(f))
