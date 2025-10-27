"""
Objects used to neatly contain coordinates, priority queue elements, and results
"""
from enum import Enum

class Mode(Enum):
    """
    Algorithm and neighbor check mode labels
    """
    BASIC = "Basic A*"
    SCREENED = "Screened A*"
    DIJKSTRA = "Dijkstra's"
    GREEDY = "Greedy Best-First"

class Coord:
    """
    Neatly contain cell coordinates for easy x,y referencing
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Coord) \
            and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

class FrontierObj:
    """
    Couple f- and g-scores to cell coordinates and enforce min-heap ordering by 
    f-score
    """
    def __init__(self, f: float, g: float, pos: Coord):
        self.f = f
        self.g = g
        self.pos = Coord(pos.x,pos.y)
    def __lt__(self, other):
        # Enforce min-heap comparison
        return (self.f) < (other.f)

class Result:
    """
    Neatly package the search cloud, frontier upon completion, and the found
    path itself
    """
    def __init__(self, mode: Mode):
        self.mode: Mode = mode
        self.path: list = []
        self.rim: set = set()
        self.cloud: set = set()
