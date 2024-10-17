#!/usr/bin/python3

from sys import argv

from calix.cx_detail import cx
from calix.ont_detail import ont
from calix.connection import calix_e9
from calix.affected_decorator import affected_decorator


b = cx("Ingram-E9-1", "3987")
print(b)


@affected_decorator
def f(a, b, c):
    pass


f(
    "Ingram-E9-1",
    ["13.107546", "13.105931", "13.67267", "13.61459"],
    ["6979", "11833", "3987", "7692"],
)
