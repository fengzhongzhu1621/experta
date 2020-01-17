# -*- coding: utf-8 -*-

from functools import update_wrapper
import inspect


class DefFacts:
    """返回需要添加到引擎中的Facts

     - 所有yield的fact都会使用declare添加到工作内存
     - 每次reset()会重新调用

    Examples:

        @DefFacts()
    def _initial_action(self):
        yield Fact(action="greet")
    """
    def __new__(cls, nonexpected=None, order=0):
        """创建对象并返回对象，当返回对象时会自动调用__init__方法进行初始化 ."""
        obj = super(DefFacts, cls).__new__(cls)

        if nonexpected is not None:
            raise SyntaxError("DefFacts must be instanced to allow decoration")

        obj.__wrapped = None
        obj._wrapped_self = None
        obj.order = order

        return obj

    @property
    def _wrapped(self):
        return self.__wrapped

    @_wrapped.setter
    def _wrapped(self, value):
        # 如何判断一个函数是否是一个特殊的 generator 函数
        if inspect.isgeneratorfunction(value):
            self.__wrapped = value
            return update_wrapper(self, self.__wrapped)
        else:
            raise TypeError("DefFact can only decorate generators.")

    def __repr__(self):  # pragma: no cover
        return "DefFacts(%r)" % (self._wrapped, )

    def __call__(self, *args, **kwargs):
        if self._wrapped is not None:
            if self._wrapped_self is None:
                gen = self._wrapped(*args, **kwargs)
            else:
                gen = self._wrapped(self._wrapped_self, *args, **kwargs)
            return (x.copy() for x in gen)
        elif not args:
            raise RuntimeError("Usage error.")
        else:
            # 获取装饰的函数，调用@_wrapped.setter
            self._wrapped = args[0]
            return self

    def __get__(self, instance, owner):
        """在任何特性被读取时调用 ."""
        self._wrapped_self = instance
        return self
