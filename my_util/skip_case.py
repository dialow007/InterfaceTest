from inspect import isfunction
from functools import wraps
import unittest


def skipIf(exp, reason):
    def wraper_func(test_func):
        @wraps(test_func)
        def func(self):
            if isfunction(exp):
                res = exp()
                if res:
                    self.skipTest(reason)
                    return
                else:
                    return test_func(self)
            else:
                raise TypeError('条件必须是函数')
                return
        return func
    return wraper_func

