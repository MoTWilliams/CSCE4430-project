# pylint: disable=missing-docstring
from math import sqrt

from map_const import G
from custom_types import Coord

EPS = 1e-9

def euc_dist(src: Coord, dest: Coord):
    dx = dest.x - src.x
    dy = dest.y - src.y
    return sqrt(dx*dx + dy*dy)

def h(current):
    return euc_dist(current, G)

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def build_rim(open_set, closed):
    rim = set()

    for obj in open_set:
        if not obj.pos in closed:
            rim.add(obj.pos)

    return rim
