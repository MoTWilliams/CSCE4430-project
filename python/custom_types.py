# pylint: disable=missing-docstring
from enum import Enum

class Mode(Enum):
    BASIC = 0
    SCREENED = 1

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Coord) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

class FrontierObj:
    def __init__(self, f: float, g: float, pos: Coord):
        self.f = f
        self.g = g
        self.pos = Coord(pos.x,pos.y)
    def __lt__(self, other):
        # Enforce min-heap comparison
        return (self.f) < (other.f)

class Result:
    def __init__(self):
        self.path: list = []
        self.rim: set = set()
        self.cloud: set = set()
