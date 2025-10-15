# pylint: disable=missing-docstring

from termcolor import colored as cd

from a_star_algo import a_star
from screened_a_star_algo import screened_a_star
from mod_a_star_algo import mod_a_star
from map_const import W, H, S, G, is_wall
from custom_types import Coord, Result

def print_result(res: Result):
    for y in reversed(range(H)):
        for x in range(W):
            c = Coord(x,y)
            if is_wall(c):
                print(cd("██", "white"),end="")
            elif c == S:
                print(cd("██", "green"),end="")
            elif c == G:
                print(cd("██", "red"),end="")
            elif c in res.path:
                print(cd("██", "light_blue"),end="")
            elif c in res.rim:
                print(cd("██", "light_yellow"),end="")
            elif c in res.cloud:
                print(cd("██", "dark_grey"),end="")
            else:
                print(cd("██", "light_green"),end="")
        print()

print_result(a_star())
print()
print_result(screened_a_star())
print()
print_result(mod_a_star())
